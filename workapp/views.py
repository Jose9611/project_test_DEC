
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import permissions
from .models import Add_edit_del_date
from .serializers import TaskSerializer
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer,UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
#from .permissions import CustomPermission



@api_view(['POST','GET'])
#@permission_classes([IsAuthenticated,])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Email or Password is Incorrect'}, status=400)

    else:

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
class TodoListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self,request, todo_id):
        try:
            item = Add_edit_del_date.objects.get(id=todo_id,user_id=request.user.id)
            serializer = TaskSerializer(item, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskSerializer.DoesNotExist:
            return None


    # 1. List all
    def get(self, request,todo_id='', *args, **kwargs):

        if todo_id:
            items = Add_edit_del_date.objects.filter(user_id=request.user.id,id=todo_id)
        else:
            items = Add_edit_del_date.objects.filter(user_id=request.user.id)
        serializer = TaskSerializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'task': request.data.get('task'),
            'description': request.data.get('description'),
            'user': request.user.id
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,todo_id, *args, **kwargs):
        if todo_id:

            task_obj = Add_edit_del_date.objects.filter(id=todo_id).first()
            task_obj.task = request.data.get('task')
            task_obj.description = request.data.get('description')
            task_obj.save()
        if task_obj:
           serializer = TaskSerializer(task_obj)
           return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(data=[], status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *args, **kwargs):

        todo_instance = Add_edit_del_date.objects.filter(user_id=request.user.id,id=todo_id).first()
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )



