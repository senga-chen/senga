<template>
  <div>
    聊天室
  </div>
</template>

<script>
    import Cookies from 'js-cookie';

    export default {
        name: "chatRoom",
        data (){
            return {
                token: ""
            }
        },
        beforeCreate() {
            let token = Cookies.get("token")
            if (!token || token === "undefined"){
              this.$store.commit('logout', this);
              this.$router.push({
                name: 'login'
              });
            }else {
              this.token = token;
            }
        }
    }
</script>

<style scoped>

</style>
