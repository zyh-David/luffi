<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
        <h3 class="cart-top">购物车结算 <span>共1门课程</span></h3>
        <div class="cart-title">
           <el-row>
             <el-col :span="2">&nbsp;</el-col>
             <el-col :span="10">课程</el-col>
             <el-col :span="8">有效期</el-col>
             <el-col :span="4">价格</el-col>
           </el-row>
        </div>
        <div class="cart-item" v-for="course in course_list">
          <el-row>
             <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
             <el-col :span="10" class="course-info">
               <img :src="course.course_img" alt="">
                <span>{{course.course_name}}</span>
             </el-col>
             <el-col :span="8"><span>{{course.expire_text}}</span></el-col>
             <el-col :span="4" class="course-price">原价 ¥{{course.price.toFixed(2)}}</el-col>
           </el-row>
        </div>
        <!-- 优惠券和积分相关代码 -->
        <div class="discount">
          <div id="accordion">
            <div class="coupon-box">
              <div class="icon-box">
                <span class="select-coupon">使用优惠劵：</span>
                <a class="select-icon unselect" :class="use_coupon?'is_selected':''" @click="use_coupon=!use_coupon"><img class="sign is_show_select" src="../../static/image/12.png" alt=""></a>
                <span class="coupon-num">有{{coupon_list.length}}张可用</span>
              </div>
              <p class="sum-price-wrap">商品总金额：<span class="sum-price">¥ {{total_price.toFixed(2)}}元</span></p>
            </div>
            <div id="collapseOne" v-if="use_coupon">
              <ul class="coupon-list" v-if="coupon_list.length>0">
                <li class="coupon-item"v-for="(item,key) in coupon_list"
                @click="check_disable(item.start_time,item.now_time,item.id)"
                    :class="check_coupon(item.start_time,item.now_time,item.id, coupon)">
                  <p class="coupon-name">{{item.coupon.name}}</p>
                  <p class="coupon-condition" v-if="item.coupon.condition>0">满{{item.coupon.condition}}元可以使用</p>
                  <p class="coupon-condition" v-else>没有使用条件</p>
                  <p class="coupon-time start_time">开始时间：{{item.start_time.replace("T"," ")}}</p>
                  <p class="coupon-time end_time">过期时间：{{item.end_time}}</p>
                </li>
              </ul>
              <div class="no-coupon" v-else>
                <span class="no-coupon-tips">暂无可用优惠券</span>
              </div>

            </div>
          </div>
          <div class="credit-box">
            <label class="my_el_check_box"><el-checkbox class="my_el_checkbox" v-model="use_credit"></el-checkbox></label>
            <p class="discount-num1" >使用我的贝里</p>
            <p class="discount-num2" ><span>总积分：{{user_credit}}抵扣 <el-input-number @change="handleChange"  v-model="credit" :min="0" :max="parseInt(user_credit)" label="请填写积分"></el-input-number>，本次花费以后，剩余{{parseInt(user_credit-credit)}}积分</span></p>
          </div>
        </div>

        <div class="calc">
            <el-row class="pay-row">
              <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
              <el-col :span="8">
                <span class="alipay"><img src="/static/image/alipay2.png" alt=""></span>
                <span class="alipay wechat"><img src="/static/image/wechat.png" alt=""></span>
              </el-col>
              <el-col :span="8" class="count">实付款： <span>¥{{total_price-coupon_price-credit_price}}</span></el-col>
              <el-col :span="4" class="cart-pay"><span @click="gotopay">支付宝支付</span></el-col>
            </el-row>
        </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  export default {
    name:"Order",
    data(){
      return {
          coupon:0,

        course_list: [],
        total_price: 0,
        coupon_price: 0,
        credit_price: 0,
        pay_type: 1,
        token:'',
        use_coupon:false, //用户是否选择使用优惠券
        use_credit:false, //用户是否选择使用积分
        user_credit:1000,
        credit: 0,
        max_credit:0,
        coupon_list:[],
      }
    },
    components:{
      Header,
      Footer,
    },
    created(){
        this.check_user();
        this.get_selected_course();
        this.get_user_coupon_list();
    },
    watch:{
        use_coupon(){
            if(!this.use_coupon){
                this.coupon=0;
            }
        },
        coupon(){
           this.use_credit = false; // 当用户使用优惠券时，关闭积分兑换~
            // 在用户选择不同优惠券时，计算当前优惠券产生的抵扣金额
          　this.get_coupon_price();
        },
          use_cerdit(){
            if (!this.use_credit){
                this.credit = 0; //当用户收起积分选项，表示取消使用积分，当前抵扣等于０
            }
          },
          credit(){
            this.check_credit();
            // 在用户调整本次订单兑换的积分时，计算当前积分抵扣的金额
            this.get_credit_price();
          }
      },
    methods: {
      check_user(){
        this.token = this.$settings.check_user_login();
        if (!this.token){
            let self = this;
            this.$alert('对不起,你尚未登录！无法访问购物车！','路飞学城',{
                callback(){
                    self.$route.push('/user/login');
                }
            })
        }
        // 登录状态获取用户积分
        this.user_credit = sessionStorage.user_credit||localStorage.user_credit
      },
      get_selected_course(){
      // 获取购物车勾选的商品

          this.$axios(`${this.$settings.Host}/cart/order/`,{
              headers:{
                  Authorization: 'jwt ' + this.token,
              }
          }).then(response=>{
              this.course_list = response.data;
              for(let item of this.course_list){
                this.total_price = this.total_price + item.price;
              }
        console.log(this.total_price)
          }).catch(error=>{
              let self = this;
              this.$alert('获取购物车数据失败！请联系客服人员！','路飞学城',{
                  callback(){
                      self.$router.go(-1)
                  }
              })
          })
      },
      // 提交结算,生成订单
      gotopay(){
        this.$axios.post(`${this.$settings.Host}/order/`,{
            headers: {
                "Authorization":"jwt " + this.token
            }
        }).then(response=>{

        }).catch(error=>{
            console.log(error.response)
        })
      },
        check_disable(start_time, now_time, coupon_id){
          console.log(new Date(start_time)-0)
          // 判断当前优惠券是否可用
          start_time = (new Date(start_time) - 0) / 1000;

          if( start_time > now_time ){
              return false;
          }

          this.coupon = coupon_id;

        },
        check_coupon(start_time, now_time, coupon_id, current_coupon){
          //判断商品的是否到了可使用的时间
          start_time = (new Date(start_time) -0) /1000;
          if(start_time >now_time){
              return "disable"; // 当前优惠券不可用
          }
          //判断是否是选中的优惠券，是高亮
          if(current_coupon === coupon_id){
              return "active";
          }
        },
        use_coupon(){
          if(!this.use_coupon){
              this.coupon = 0; // 当用户收起优惠券列表，则表示取消使用优惠券，当前选择的优惠券归0重置.
          }
      },
        check_credit(){
          // 判断积分的时候，是否超额
          // 先比较用户积分和实付金额，提取最小数值
          let credit_money = sessionStorage.credit_money||localStorage.credit_money;
          let order_credit = Math.floor((this.total_price - this.coupon_price) * credit_money);
          let min_credit = 0;
          if(order_credit > this.user_credit){
              min_credit = this.user_credit;
          }else{
              min_credit = order_credit;
          }

          if(this.credit >= min_credit){
              this.credit = min_credit;
          }

        },

        handleChange(){

        },
        get_credit_price(){
          this.credit_price = this.credit/this.credit_money
        },
        get_coupon_price(){

        },

        get_user_coupon_list(){
          // 获取购物车中勾选的商品信息
          console.log(this.token);
          this.$axios.get(`${this.$settings.Host}/coupon/`,{
              headers: {
                "Authorization":"jwt " + this.token
            }
          }).then(response=>{
              this.coupon_list = response.data;
              // 计算当前所有商品价格
              console.log(this.coupon_list)
          })
        },
    }

  }
</script>

<style scoped>
.cart{
    margin-top: 80px;
  }
  .cart-info{
    overflow: hidden;
    width: 1200px;
    margin: auto;
  }
  .cart-top{
    font-size: 18px;
    color: #666;
    margin: 25px 0;
    font-weight: normal;
  }
  .cart-top span{
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
  }
  .cart-title{
    background: #F7F7F7;
    height: 70px;
  }
  .calc{
    margin-top: 25px;
    margin-bottom: 40px;
  }

  .calc .count{
    text-align: right;
    margin-right: 10px;
    vertical-align: middle;
  }
  .calc .count span{
    font-size: 36px;
    color: #333;
  }
  .calc .cart-pay{
    margin-top: 5px;
    width: 110px;
    height: 38px;
    outline: none;
    border: none;
    color: #fff;
    line-height: 38px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
  }
  .cart-item{
    height: 120px;
    line-height: 120px;
    margin-bottom: 30px;
  }
  .course-info img{
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
    float: left;
  }
  .course-info::after{
    clear: both;
  }
  .course-info .course_text{
    float: left;
    line-height: 36px;
  }
  .course-info .course_text .discount_name{
    color: #ffc210;
    display: block;
  }
  .course-price p{
    line-height: 36px;
  }
  .course-price .original_price{
    color: #9b9b9b;
  }
  .alipay{
    display: inline-block;
    height: 48px;
  }
  .alipay img{
    height: 100%;
    width:auto;
  }

  .pay-text{
    display: block;
    text-align: right;
    height: 100%;
    line-height: 100%;
    vertical-align: middle;
    margin-top: 20px;
  }
  /** 优惠券 **/
.coupon-box{
  text-align: left;
  padding-bottom: 22px;
  padding-left:30px;
  border-bottom: 1px solid #e8e8e8;
}
.coupon-box::after{
  content: "";
  display: block;
  clear: both;
}
.icon-box{
  float: left;
}
.icon-box .select-coupon{
  float: left;
  color: #666;
  font-size: 16px;
}
.icon-box::after{
  content:"";
  clear:both;
  display: block;
}
.select-icon{
  width: 20px;
  height: 20px;
  float: left;
}
.select-icon img{
  max-height:100%;
  max-width: 100%;
  margin-top: 2px;
  transform: rotate(-90deg);
  transition: transform .5s;
}
.is_show_select{
  transform: rotate(0deg)!important;
}
.coupon-num{
    height: 22px;
    line-height: 22px;
    padding: 0 5px;
    text-align: center;
    font-size: 12px;
    float: left;
    color: #fff;
    letter-spacing: .27px;
    background: #fa6240;
    border-radius: 2px;
    margin-left: 20px;
}
.sum-price-wrap{
    float: right;
    font-size: 16px;
    color: #4a4a4a;
    margin-right: 45px;
}
.sum-price-wrap .sum-price{
  font-size: 18px;
  color: #fa6240;
}

.no-coupon{
  text-align: center;
  width: 100%;
  padding: 50px 0px;
  align-items: center;
  justify-content: center; /* 文本两端对其 */
  border-bottom: 1px solid rgb(232, 232, 232);
}
.no-coupon-tips{
  font-size: 16px;
  color: #9b9b9b;
}
.credit-box{
  height: 30px;
  margin-top: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-end
}
.my_el_check_box{

  position: relative;
}
.my_el_checkbox{
  margin-right: 10px;
  width: 16px;
  height: 16px;
}
.discount{
  overflow: hidden;
}
.discount-num1{
  color: #9b9b9b;
  font-size: 16px;
  margin-right: 45px;
}
.discount-num2{
  margin-right: 45px;
  font-size: 16px;
  color: #4a4a4a;
}
.sun-coupon-num{
  margin-right: 45px;
  margin-bottom:43px;
  margin-top: 40px;
  font-size: 16px;
  color: #4a4a4a;
  display: inline-block;
  float: right;
}
.sun-coupon-num span{
  font-size: 18px;
  color: #fa6240;
}
.coupon-list{
  margin: 20px 0;
}
.coupon-list::after{
  display: block;
  content:"";
  clear: both;
}
.coupon-item{
  float: left;
  margin: 15px 8px;
  width: 180px;
  height: 100px;
  padding: 5px;
  background-color: #fa3030;
  cursor: pointer;
}
.coupon-list .active{
  background-color: #fa9000;
}
.coupon-list .disable{
  cursor: not-allowed;
  background-color: #fa6060;
}
.coupon-condition{
  font-size: 12px;
  text-align: center;
  color: #fff;
}
.coupon-name{
  color: #fff;
  font-size: 24px;
  text-align: center;
}
.coupon-time{
  text-align: left;
  color: #fff;
  font-size: 12px;
}
.unselect{
  margin-left: 0px;
  transform: rotate(-90deg);
}
.is_selected{
  transform: rotate(-1turn)!important;
}
[class*=" el-icon-"], [class^=el-icon-]{
  font-size: 12px;
}
</style>
