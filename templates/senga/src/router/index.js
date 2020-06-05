import Vue from 'vue'
import Router from 'vue-router'
import chatRoom from "../views/chatRoom/chatRoom";
import login from '../views/login/login'

Vue.use(Router)

export default new Router({
  mode: "hash",
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
