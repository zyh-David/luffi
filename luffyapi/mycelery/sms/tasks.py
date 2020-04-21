# celery的任务必须写在tasks.py的文件中，别的文件名称不识别
import logging

from luffyapi.settings import constants
from mycelery.main import app
from .yuntongxun.sms import CCP

log = logging.getLogger('django')


@app.task(name="send_sms")
def send_sms(mobile, sms_code):
    """发送短信"""
    ccp = CCP()
    ret = ccp.send_template_sms(mobile, [sms_code,constants.SMS_EXPIRE_TIME//60],constants.SMS_TEMPLATE_ID)
    if ret == -1:
        log.error('用户注册短信发送失败！手机号：%s' % mobile)
        return {'message':'短信发送失败！请刷新页面重新尝试发送或联系客服工作人员！'}

