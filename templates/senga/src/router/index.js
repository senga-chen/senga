import Vue from 'vue'
import Router from 'vue-router'
import chatRoom from "../views/chatRoom/chatRoom";
import login from '../views/login/login'
// import chatRoom from '/view/chatRoom/chatRoom'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/chatRoom',
      name: 'chatRoom',
      component: chatRoom
    }
  ]
})
