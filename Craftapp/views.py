from rest_framework.views import APIView
from rest_framework.response import Response
from Craftapp.serializers import *
from rest_framework import status
from django.contrib.auth import authenticate, login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Craftapp.utils import *
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle




# Create your views here.
"""API for User Signup"""
class SignupView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"User Register Successfully","code":200},status=status.HTTP_200_OK)
       
        dynamic_key = next(iter(serializer.errors))
        return Response({"code":400,"error":serializer.errors[dynamic_key][0]},status=status.HTTP_200_OK)



"""API for User Login"""
class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')    
        password = request.data.get('password')
        user=authenticate(username=email, password=password)
        if user:
            login(request, user)      
            usr=Token.objects.filter(user_id=user.id)
            if not usr:
                user_token=Token.objects.create(user=user) 
            else:
                user_token=Token.objects.filter(user_id=user.id).values_list("key",flat=True)[0]
            data={"firstname":user.first_name,
                    "lastname":user.last_name,
                    "email":user.email,
                    "breweries_id":user.brewery
            }
            return Response({'success':"Login Successfully",'token':str(user_token),"code":200,"data":data}, status=status.HTTP_200_OK)  
        else:
            return Response({'error': 'Invalid credentials',"code":400}, status=status.HTTP_200_OK)
        


"""API for User Logout"""
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"success":'User Logged out successfully'},status=status.HTTP_200_OK)
    


"""API TO GET BREWERIES DATA"""
class BreweriesView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def get(self,request):
        try:
            brewery_data=breweries(request)
            return Response({"code":200,"data":brewery_data[0]},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)


"""API TO GET TRAIL DATA"""
class TrailView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def get(self,request):
        try:
            trails_data=trails(request)   
            return Response({"code":200,"data":trails_data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
       
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)


"""API TO GET PARTICIPANTS DATA"""
class ParticipantsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def get(self,request):
        try:
            participants_data=participants(request)
            return Response({"code":200,"data":participants_data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)
        

"""API TO GET PARTICIPANTS POINTS DATA"""
class ParticipantsPointsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def get(self,request):
        try:
            partic_data=participantspoints(request)
            return Response({"code":200,"data":partic_data},status=status.HTTP_200_OK)
        except Exception as e:
           
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)
        


"""API TO GET VISIT DATA"""
class VisitView(APIView):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    permission_classes=[IsAuthenticated]                                                                                                                                                                                                                                                                                                                                                                                                                            
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def get(self,request):
        try:
            visit_data=visit(request)    
            return Response({"code":200,"data":visit_data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)
        

"""API TO CHANGE PASSWORD"""
class ChangePassword(APIView):
    permission_classes=[IsAuthenticated]                                                                                                                                                                                                                                                                                                                                                                                                                            
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'message': 'Password changed successfully',"code":200}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.',"code":200}, status=status.HTTP_200_BAD_REQUEST)
        return Response({"error":"Unable to change password","code":400}, status=status.HTTP_400_BAD_REQUEST)
    

"""API TO SHOW COUNT OF ACTIVE USER"""
class ActiveUser(APIView):
    permission_classes=[IsAuthenticated]                                                                                                                                                                                                                                                                                                                                                                                                                            
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'
    def get(self,request):
        try:
            trails_data=trails(request)   
            active_trails_data=active_trails(request)   
            count=0
            for i in trails_data:
                val=[k for k in active_trails_data.json()["items"] if i["mini_tour"]==k["sd82de27d5"]]
                if val: 
                    count=count+1

            active_user={
                "active_count":count
            }
            return Response({"code":200,"data":active_user},status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)
        

"""API TO GET TRAILS ANALYTICS DATA"""
class TrailsAnalytics(APIView):
    permission_classes=[IsAuthenticated]                                                                                                                                                                                                                                                                                                                                                                                                                            
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'
    def get(self,request):
        try:
            trails_data=trails(request)   
            active_trails_data=active_trails(request)   
            for k in active_trails_data.json()["items"]:
                val=[round(i["title_submenu"]["breweries_completed"]["count"]/int(i["location_to_complete"])*100,2) for i in trails_data if i["mini_tour"]==k["sd82de27d5"]]
        
            breweries_analytics={
                "breweries_percentage":val
            }
            return Response({"code":200,"data":breweries_analytics},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)
        


class BreweriesName(APIView):
    permission_classes=[IsAuthenticated]                                                                                                                                                                                                                                                                                                                                                                                                                            
    authentication_classes=[TokenAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'custom'

    def get(self,request):
        try:
            breweriesname=breweries(request)
            bar_name={"bar_name":breweriesname[1]}
            return Response({"code":200,"data":bar_name},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"code":400,"error":"Unable to fetch data"},status=status.HTTP_200_OK)
            
            




