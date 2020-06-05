<style lang="less">
  @import './login.less';
</style>

<template>
  <div @keydown.enter="handleSubmit" style="width: 100%;height: 100%;display: flex;align-items: center;">
    <div class="long_left"></div>
    <div class="login_right">
      <div class="login_content">
        <div class="login_title_box">
          <div class="login_title">
            LOGIN
            <span>欢迎登录</span>
          </div>
        </div>
        <div class="login_input">
          <form ref="loginForm" :model="form" :rules="rules">
            <input v-model="form.username" placeholder="请输入用户名">
            <input v-model="form.password" placeholder="请输入密码">
          </form>
        </div>
        <Button @click="handleSubmit" class="login_btn">登录</Button>
      </div>
    </div>
  </div>

</template>

<script>
  import Cookies from 'js-cookie';
  import {LoginH} from '../../fetch/fetch'

  export default {
    name: "login",
    data () {
      return {
        form: {
          username: '',
          password: ''
        },
        rules: {
          password: [
            { required: true, type: 'string', message: '用户名不能为空', trigger: 'blur' }
          ],
          username: [
            { required: true, type: 'string', message: '密码不能为空', trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      handleSubmit () {
          let password = this.form.password;
          let username = this.form.username;
          let param = {username:username, password: password};
          LoginH(param).then( response=>{
            if(response.error_code != 0){
              // this.$Notice.warning({
              //   title: response.error_msg,
              //   duration:5
              // });
              alert(response.error_msg)
            }else {
              // console.log(response)
              let username = response.user.name;
              let token = response.user.token;
              let cover = response.user.cover;
              let user_id = response.user.id;
              if (!cover){
                cover = "http://s1.wmlives.com/data/dongci/user_cover/20180503155855170276.jpg!cover_img_thumbnail"
              }
              let attributes = {};
              attributes.expires = 1;
              console.log(attributes)
              Cookies.set('user_id', user_id, attributes);
              Cookies.set('user', username, attributes);
              Cookies.set('token', token, attributes);
              Cookies.set('cover', cover, attributes);
              this.$router.push({
                name: 'chatRoom'
              });
            }
          }).catch(error => {
            console.log(error)
          });
      }
    },
    mounted () {
    }
  };
</script>

<style>

</style>
