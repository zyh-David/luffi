import logging

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from course.models import Course,CourseExpire

from luffyapi.settings import constants

log = logging.getLogger("django")


class CartAPIView(ViewSet):
    """购物车"""
    permission_classes = [IsAuthenticated]

    def add(self, request):
        """添加商品到购物车"""
        # 接受客户提交的参数[用户ID, 课件ID, 勾选状态, 有效期选项]
        course_id = request.data.get('course_id')
        user_id = request.user.id
        # 设置默认值
        selected = True
        expire = 0
        # 校验参数
        try:
            course = Course.objects.get(is_show=True, is_deleted=False, id=course_id)
        except Course.DoesNotExist:
            return Response({'message':'参数有误！课程不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取redis连接对象
        redis_conn = get_redis_connection('cart')
        # 保存数据到redis
        try:
            pipe = redis_conn.pipeline()
            pipe.multi()
            pipe.hset('cart_%s' % user_id, course_id, expire)
            pipe.sadd('selected_%s' % user_id, course_id)
            pipe.execute()

            # 查询购物车中的商品总数
            course_len = redis_conn.hlen('cart_%s' % user_id)
        except:
            log.error('购物车数据库存储错误！')
            return Response({'message': '参数有误！购物车添加商品失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        cart_num = redis_conn.hlen("cart_%s" % user_id)
        # 返回结果[当前购物车中的商品总数]
        return Response({'cart_num': cart_num, 'length': course_len}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """购物车商品列表"""
        # 1.获取当前用户的id
        user_id = request.user.id

        # 2.在redis中获取当前用户的购物车商品信息
        redis_conn = get_redis_connection('cart')

        cart_hash = redis_conn.hgetall("cart_%s" % user_id)
        selected_set = redis_conn.smembers('selected_%s' % user_id)
        # 要返回给客户端的数据
        data = []

        # 3.在mysql中根据购物车的商品id获取商品其他详情信息
        for course_id_bytes, expire_time_bytes in cart_hash.items():
            course_id = course_id_bytes.decode()
            expire_time = int(expire_time_bytes.decode())

            # try:
            course = Course.objects.get(pk=course_id)
            data.append({
                "course_name": course.name,
                "course_id": course.id,
                "course_img": constants.SERVER_IMAGE_URL + course.course_img.url,
                "price": course.price,
                "selected": True if course_id_bytes in selected_set else False,
                "expire_list": course.get_expire_list,
                "expire": int(expire_time),
            })
            # except Course.DoesNotExist:
            #     pass
        return Response(data)

    def change_course_status(self, request):
        """更新用户购物车的商品勾选状态"""
        # 获取客户端的信息
        user_id = request.user.id
        course_id = request.data.get('course_id')
        selected = request.data.get('selected')

        # 连接redis,修改购物车中的商品勾选状态
        redis_conn = get_redis_connection('cart')
        if selected:
            redis_conn.sadd('selected_%s' % user_id, course_id)
        else:
            """取消勾选状态"""
            redis_conn.srem('selected_%s' % user_id, course_id)

        return Response({'message': '切换商品勾选成功！'})


    def change_course_expire(self,request):
        """更新用户购物车商品的有效期"""
        # 获取客户端的信息[courese_id, user_id, expre_time]
        user_id = request.user.id
        course_id =request.data.get('course_id')
        expire_time = request.data.get('expire_time')

        # 连接redis，修改购物车中商品的有效期选项
        redis_conn = get_redis_connection("cart")
        redis_conn.hset("cart_%s" % user_id, course_id, expire_time)
        return Response({"message": "切换商品有效期选项成功！"})

    def delete(self,request):
        """购物车商品的删除"""
        # 1.获取客户端的信息[course_id, user_id]
        user_id= request.user.id
        course_id = request.query_params.get('course_id')
        print(course_id)
        # 2. 连接redis, 执行删除操作
        redis_conn = get_redis_connection('cart')
        pipe = redis_conn.pipeline()
        pipe.multi()
        pipe.hdel('cart_%s' % user_id, course_id)
        pipe.srem('selected_%s' % user_id, course_id)
        pipe.execute()

        return Response({"message": "delete success!"}, status=status.HTTP_204_NO_CONTENT)

    def get_selected_course(self, request):
        user_id = request.user.id

        redis_conn = get_redis_connection('cart')
        cart_hash = redis_conn.hgetall('cart_%s' % user_id)
        course_id_list = redis_conn.smembers('selected_%s' % user_id)

        data = []

        for course_id_byte in course_id_list:
            course_id = course_id_byte.decode()
            course_time = int(cart_hash.get(course_id_byte).decode())

            course = Course.objects.get(pk=course_id)
            course.real_price(course_time)
            CourseExpire.get_expire_text(course_id, course_time)
            data.append({
                "course_id": course.id,
                "course_img": constants.SERVER_IMAGE_URL + course.course_img.url,  # 返回图片的url地址
                "course_name": course.name,
                "price": course.real_price(course_time),  # 商品原价
                "real_price": 0.00,  # 折扣以后的价格
                "expire_text": CourseExpire.get_expire_text(course_id, course_time)
            })

        return Response(data)
