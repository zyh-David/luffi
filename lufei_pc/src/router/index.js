import Vue from 'vue'
import Router from 'vue-router'

import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import Detail from "../components/Detail";
import Cart from "../components/Cart";
import Order from "../components/Order";


Vue.use(Router)

export default new Router({
  // 设置路由模式为‘history’,可以去掉默认的#
  mode: 'history',

  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/user/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register/',
      name:'Register',
      component: Register,
    },
    {
      path: '/course/',
      name: 'Course',
      component: Course,
    },
    {
      path: '/course/:id',
      name: 'Detail',
      component: Detail,
    },
    {
      path: '/cart/',
      name: 'Cart',
      component: Cart,
    },
    {
      path: '/order/',
      name: 'Order',
      component: Order,
    },
  ]
})
