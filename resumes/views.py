from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.files.base import ContentFile

from .models import MatchResult
from .forms import ResumeForm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors

from io import BytesIO
import datetime


def home(request):
    return render(request, 'resumes/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form and try again.')
    else:
        form = UserCreationForm()

    return render(request, 'resumes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('match_resume')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'resumes/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text


def calculate_match_score(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = round(similarity[0][0] * 100, 2)
    return score


@login_required
def match_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES['resume']
        job_description = request.POST['job_description'].strip()
        resume_text = extract_text_from_pdf(resume_file)
        score = calculate_match_score(resume_text, job_description)

        # Generate PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Resume Matcher Result")
        p.drawString(100, 700, f"Match Score: {score}%")
        p.drawString(100, 650, f"Job Description: {job_description[:50]}...")
        p.save()
        buffer.seek(0)
        pdf_content = ContentFile(buffer.read())
        pdf_filename = f'result_{request.user.username}_{resume_file.name}.pdf'

        # Save MatchResult
        match = MatchResult.objects.create(
            user=request.user,
            resume_file=resume_file,
            job_description=job_description,
            score=score,
        )
        match.result_pdf.save(pdf_filename, pdf_content)
        match.save()

        # Show result with pie chart
        return render(request, 'resumes/result.html', {
            'score': score,
            'match': match
        })

    return render(request, 'resumes/form.html')



@login_required
def match_history(request):
    match_results = MatchResult.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'resumes/history.html', {'match_results': match_results})


@login_required
def profile_view(request):
    user = request.user
    match_count = MatchResult.objects.filter(user=user).count()
    return render(request, 'resumes/profile.html', {'user': user, 'match_count': match_count})


def generate_pdf(result):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 80, "Resume Match Report")

    p.setStrokeColor(colors.grey)
    p.setLineWidth(1)
    p.line(50, height - 90, width - 50, height - 90)

    p.setFont("Helvetica", 12)
    y = height - 130
    line_height = 20

    p.drawString(80, y, f"Resume Name: {result.resume_file.name}")
    y -= line_height
    p.drawString(80, y, f"Match Score: {result.score}%")
    y -= line_height

    truncated_desc = result.job_description[:300] + ("..." if len(result.job_description) > 300 else "")
    p.drawString(80, y, "Job Description:")
    y -= line_height
    text = p.beginText(100, y)
    text.setFont("Helvetica", 11)
    for line in truncated_desc.split('\n'):
        text.textLine(line)
    p.drawText(text)

    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.darkgrey)
    p.drawString(80, 40, f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    p.showPage()
    p.save()

    buffer.seek(0)
    result.result_pdf.save(f"match_result_{result.id}.pdf", ContentFile(buffer.read()))
