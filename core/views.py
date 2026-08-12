from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class EducationalHubView(APIView):
    """Serves static educational content to the frontend."""
    permission_classes = [AllowAny]

    def get(self, request):
        content = {
            "digital_literacy": [
                {
                    "title": "How to Spot a Deepfake", 
                    "content": "Look for unnatural eye blinking, weird lighting, and mismatched audio syncing."
                },
                {
                    "title": "Verify Before You Share", 
                    "content": "Always check multiple reputable news sources before forwarding a WhatsApp broadcast."
                }
            ],
            "tfgbv_resources": [
                {
                    "title": "Understanding TFGBV", 
                    "content": "Tech-Facilitated Gender-Based Violence includes targeted online harassment, doxxing, and non-consensual image sharing."
                },
                {
                    "title": "How to Get Help", 
                    "content": "If you are a victim, use our secure reporting form. Your data is encrypted and only seen by specialized legal experts."
                }
            ]
        }
        return Response(content)