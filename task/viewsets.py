from rest_framework import viewsets
from .serializer import TaskSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, MultiPartParser

tasks = []
class TaskViewSet(viewsets.ViewSet):
    serializer_class = TaskSerializer
    http_method_names = ['post', 'get', 'patch', 'delete',]
    permission_classes = (AllowAny,)
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        request_body=TaskSerializer,
        responses={201: TaskSerializer}
    )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_task = serializer.validated_data
        new_task['id'] = len(tasks) + 1
        tasks.append(new_task)

        return Response({'message' : 'new task has been added','data' : new_task,}, status=status.HTTP_201_CREATED )
    
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        try:
                task_id = int(kwargs.get('pk')) - 1
                tasks.pop(task_id)

                return Response({'message' : 'Task has been delete', }, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'message' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=TaskSerializer,
        responses={200: TaskSerializer}
    )  
    def partial_update(self, request,**kwargs):
        try:
            task_id = int(kwargs.get('pk')) - 1
            task = tasks[task_id]
            
        except(IndexError):
             return Response({'message' : 'index is out of range'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(task, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task.update(serializer.validated_data)

        return Response({'message' : 'Task has been updated', 'data' : serializer.data}, status=status.HTTP_200_OK)
        