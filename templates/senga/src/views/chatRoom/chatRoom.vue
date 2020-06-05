<style lang="less">
  @import './chatRoom.less';
</style>

<template>
  <div id="chat_box">
    <div class="chat_top">
      <div class="top_left">
        <div class="cover">
            <user_cover :cover_path="userinfo.cover"></user_cover>
        </div>
        <div class="name">
            {{userinfo.name}}
        </div>

      </div>
      <div class="top_right">
        欢迎来到聊天室
      </div>
    </div>

    <div class="chat_content"></div>

    <div class="chat_footer"></div>
  </div>
</template>

<script>
    import user_cover from '../../components/cover'
    import Cookies from 'js-cookie';
    import user from "../../store/modules/user";

    export default {
        name: "chatRoom",
        components: {
          user_cover
        },
        data (){
            return {
                userinfo: {
                    name: "",
                    cover: "",
                    user_id: 0,
                    token: ""
                },
                socket: null
            }
        },
        methods: {
            init(){
                let name = Cookies.get("user");
                let cover = Cookies.get("cover");
                let user_id = Cookies.get("user_id");
                let token = Cookies.get("token")
                this.userinfo.cover = cover;
                this.userinfo.name = name;
                this.userinfo.user_id = user_id;
                this.userinfo.token = token;
            },
            socketConnect(){
                let url = "ws://127.0.0.1:8088/chatsocket";
                this.socket = new WebSocket(url);
                this.socket.onmessage = function(event) {
                    console.log(event)
                    this.socket.showMessage(JSON.parse(event.data));
                }
            },
            showMessage(message){
                console.log(message)
            }
        },
        beforeCreate() {
            let token = Cookies.get("token")
            if (!token || token === "undefined"){
              user.$store.commit('logout', this);
              this.$router.push({
                name: 'login'
              });
            }
        },
        mounted() {
            this.init();
            this.socketConnect();
        }
    }
</script>

<style scoped>

</style>
