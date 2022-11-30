# from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apollo.models import ApolloApp, ApolloInstance
from apollo.serializers import ApolloAppSerializer, ApolloInstanceSerializer, ApolloAuthorizedSerializer

import json
import logging
dlogger = logging.getLogger('defaultlogger')

# 基础 APIView 类
class ApolloView(APIView):
    """
    List all apollo_app instance, or create a new instance.
    """
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        apollo_app_list = ApolloApp.objects.all()
        serializer = ApolloAppSerializer(apollo_app_list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ApolloAppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(data=err.__str__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ApolloDetailView(APIView):
    """
    Retrieve, Update, Delete an apollo_app instance.
    """
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, app_id, *args, **kwargs):
        """
        :param request: HTTP request
        :param app_id: apollo app_id
        :return: HTTP Response
        """
        try:
            # apollo_app = ApolloApp.objects.get(belong_app=app_id)
            apollo_app = ApolloApp.objects.filter(belong_app=app_id)
            app_info_list = []
            for app in apollo_app:
                serializer = ApolloAppSerializer(app)
                app_info_list.append(serializer.data)
            return Response(app_info_list)
        except Exception as err:
            return Response(data=err.__str__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, app_id, *args, **kwargs):
        try:
            apollo_app_ins = ApolloApp.objects.get(
                belong_app=app_id,
                item_key=request.data['item_key']
            )
            serializer = ApolloAppSerializer(instance=apollo_app_ins, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except apollo_app_ins.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response(data=err.__str__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, app_id, *args, **kwargs):
        try:
            apollo_app_ins = ApolloApp.objects.get(
                belong_app=app_id,
                item_key=request.data['item_key']
            )
            apollo_app_ins.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ApolloApp.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# generic class-based views
from rest_framework import generics
class ApolloInstanceList(generics.ListCreateAPIView):
    queryset = ApolloInstance.objects.all()
    serializer_class = ApolloInstanceSerializer

class ApolloInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApolloInstance.objects.all()
    serializer_class = ApolloInstanceSerializer
    lookup_field = 'app_id'

class ApolloAuthorized(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, app_id, *args, **kwargs):
        try:
            request.data['app_id'] = app_id
            serializer = ApolloAuthorizedSerializer(data=request.data)
            if serializer.is_valid():
                # 授权操作
                from util.apollo_operate import ApolloClient
                apollo_client = ApolloClient()
                auth_result = apollo_client.add_authorized(**serializer.data)

                return Response(auth_result, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(data=err.__str__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
