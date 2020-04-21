import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库,类似vue组件里面的data
  state: {
      num: sessionStorage.cart_num,
  },
  // 数据操作方法,类似vue里面的methods
  mutations: {
      // 修改购物车的商品总数
    update_num(state,data){
      state.num = data;
      sessionStorage.cart_num = data;
    }
  }
});
