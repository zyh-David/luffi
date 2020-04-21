import xadmin

from .models import CourseCategory, CourseExpire, CourseDiscountType, CourseDiscount, CoursePriceDiscount, Activity


class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass
xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


from .models import Course
class CourseModelAdmin(object):
    """课程模型管理类"""
    pass
xadmin.site.register(Course, CourseModelAdmin)

from .models import Teacher
class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass
xadmin.site.register(Teacher, TeacherModelAdmin)


from .models import CourseChapter
class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass
xadmin.site.register(CourseChapter, CourseChapterModelAdmin)



from .models import CourseLesson
class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass
xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


class CorseExpireModelAdmin(object):
    """商品有效期"""
    pass
xadmin.site.register(CourseExpire, CorseExpireModelAdmin)


"""优惠相关的注册表"""
class CourseDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass
xadmin.site.register(CourseDiscountType, CourseDiscountTypeModelAdmin)

class CourseDiscountModelAdmin(object):
    """价格优惠公式"""
    pass
xadmin.site.register(CourseDiscount, CourseDiscountModelAdmin)

class CoursePriceDiscountMidelAdmin(object):
    """商品优惠和活动的关系"""
    pass
xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountMidelAdmin)

class ActivityModelAdmin(object):
    """商品活动模型"""
    pass
xadmin.site.register(Activity, ActivityModelAdmin)