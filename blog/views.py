from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import requests, os, re

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

def frontend_view(request):
    return render(request, "blog/frontend.html")

# Featherless configuration
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_API_URL = "https://api.featherless.ai/v1/completions"
FEATHERLESS_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

HEADERS = {
    "Authorization": f"Bearer rc_21380bf2f121200aafa1cba8de35d0a4400c711e10e1cf95b68c6fb606ee5778",
    "Content-Type": "application/json"
}

# Bonus AI-generated blog post
@api_view(["POST"])
def generate_post(request):
    prompt = request.data.get("prompt", "")
    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)

    payload = {
        "model": FEATHERLESS_MODEL,
        "prompt": f"Write a detailed, well-structured blog post about the following topic: {prompt}. Avoid repetition and be clear and informative.",
        "max_tokens": 300,         # limit length of the response
        "temperature": 0.6,        # controls randomness; lower is more focused
        "top_p": 0.9,              # nucleus sampling, controls diversity
        "frequency_penalty": 0.5,  # penalizes repeated tokens
        "presence_penalty": 0.5    # penalizes repeated topics/concepts
    }

    try:
        result = requests.post(FEATHERLESS_API_URL, headers=HEADERS, json=payload, timeout=20)
        result.raise_for_status()
        response = result.json()
        print("AI Response:", response)
        content = response["choices"][0]["text"].strip()

        # Clean response if it's messy
        if not content.endswith(('.', '!', '?')):
            sentences = re.split(r'(?<=[.!?])\s+', content)
            content = ' '.join(s for s in sentences if s.endswith(('.', '!', '?')))

        title = prompt.title()
        content = response["choices"][0]["text"].strip()
        post = Post.objects.create(title=title, content=content, author="AI Bot")
    
        return Response(PostSerializer(post).data)
    
    except Exception as e:
        print("Blog generation failed:", e)
        return Response({"error": "Failed to generate blog post"}, status=500)
