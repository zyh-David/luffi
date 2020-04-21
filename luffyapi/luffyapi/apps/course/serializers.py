from rest_framework import serializers

from .models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name', 'title', 'signature', 'image', 'brief']


class CourseChapterModelSerializer():
    class Meta:
        model = CourseChapter
        fields = ("id", "name", "coursesections")


class CourseModelSerializer(serializers.ModelSerializer):
    # 默认情况,序列化器转换模型数据时,默认会把外键直接转成主键ID值
    # 所以我们需要重新设置在序列化器中针对外键的序列化
    # 这种操作就是一个序列器里面调用另一个序列化器了.叫"序列化器嵌套"
    teacher = TeacherModelSerializer()
    # coursechapters = CourseChapterModelSerializer(many=True)

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "discount_name",
                  'discount_price', "teacher", "lesson_list", 'get_expire_list')


class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    """课程详情页的序列化器"""
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher",
                  "discount_name", 'discount_price', "level_text","brief", "attachment_path",
                  "course_video", 'activity_time']


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'name', 'duration', 'free_trail']


class CourseChapterSerializer(serializers.ModelSerializer):
    # coursesctions = CourseLessonSerializer(many=True)
    class Meta:
        model = CourseChapter
        fields = ["id", "name", "chapter", "summary", "lesson_list"]
