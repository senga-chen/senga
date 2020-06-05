<template>
    <img class="coverClass" :src="cover_path"/>
</template>

<script>
    export default {
        name: "user_cover",
        props: {
          cover_path: String
        }
    }
</script>

<style scoped>
.coverClass{
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
</style>
