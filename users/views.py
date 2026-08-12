from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import IncidentSerializer # Update with your actual serializer
from core.utils import sanitize_image_exif # Your EXIF scrubbing function

class IncidentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        image_file = request.FILES.get('media')

        if image_file:
            try:
                # Pass the uploaded image through your EXIF sanitization utility
                cleaned_image = sanitize_image_exif(image_file)
                # Replace the raw file with the sanitized buffer ready for Cloudinary storage
                data['media'] = cleaned_image
            except Exception as e:
                return Response(
                    {"error": f"Failed to sanitize image metadata: {str(e)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = IncidentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)