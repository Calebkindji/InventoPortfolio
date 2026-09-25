import io
import qrcode
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

User = get_user_model()


class GenerateQRCodeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username.lower().strip(), is_suspended=False)
        portfolio_url = request.build_absolute_uri(f"/u/{user.username}")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(portfolio_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#1E293B", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type="image/png")


class ExportPDFCVView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username.lower().strip(), is_suspended=False)
        profile = getattr(user, 'profile', None)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CVTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            'CVSubtitle',
            parent=styles['Heading3'],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=8
        )
        section_style = ParagraphStyle(
            'CVSection',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'CVBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155')
        )

        story = []

        # Name & Title
        full_name = user.get_full_name() or user.username
        story.append(Paragraph(full_name, title_style))
        if profile and profile.title:
            story.append(Paragraph(profile.title, subtitle_style))

        # Contact info
        contact_info = []
        if user.email:
            contact_info.append(f"Email: {user.email}")
        if profile and profile.location:
            contact_info.append(f"Localisation: {profile.location}")
        if profile and profile.github_url:
            contact_info.append(f"GitHub: {profile.github_url}")

        if contact_info:
            story.append(Paragraph(" | ".join(contact_info), body_style))
            story.append(Spacer(1, 8))

        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=10))

        # Bio
        if profile and profile.bio:
            story.append(Paragraph("<b>À propos</b>", section_style))
            story.append(Paragraph(profile.bio, body_style))
            story.append(Spacer(1, 10))

        # Skills
        if profile and profile.profile_skills.exists():
            story.append(Paragraph("<b>Compétences Clés</b>", section_style))
            skills_text = ", ".join([f"{ps.skill.name} ({ps.get_level_display()})" for ps in profile.profile_skills.select_related('skill').all()])
            story.append(Paragraph(skills_text, body_style))
            story.append(Spacer(1, 10))

        # Experiences
        experiences = user.experiences.all()
        if experiences.exists():
            story.append(Paragraph("<b>Expériences Professionnelles</b>", section_style))
            for exp in experiences:
                period = f"{exp.start_date.strftime('%b %Y')} - " + ("Présent" if exp.is_current else exp.end_date.strftime('%b %Y') if exp.end_date else "")
                exp_header = f"<b>{exp.position}</b> chez <b>{exp.company}</b> ({period})"
                story.append(Paragraph(exp_header, body_style))
                if exp.description:
                    story.append(Paragraph(exp.description, body_style))
                story.append(Spacer(1, 6))

        # Educations
        educations = user.educations.all()
        if educations.exists():
            story.append(Paragraph("<b>Formations</b>", section_style))
            for edu in educations:
                period = f"{edu.start_date.strftime('%Y')} - " + (edu.end_date.strftime('%Y') if edu.end_date else "Présent")
                edu_header = f"<b>{edu.degree}</b> - {edu.institution} ({period})"
                story.append(Paragraph(edu_header, body_style))
                story.append(Spacer(1, 4))

        doc.build(story)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="cv_{user.username}.pdf"'
        return response
