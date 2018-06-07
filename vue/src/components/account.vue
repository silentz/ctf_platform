<template lang="html">
    <div class="account">
        <div class="header">
            <h2>{{ username }}</h2>
        </div>
        <div class="content">
            
        </div>
    </div>
</template>

<script>
export default {
    name: "Account",
    computed: {
        username: function() {
            return this.$store.state.username;
        }
    }
}
</script>

<style lang="scss">
.account {
    margin: 10px;
    padding: 10px;
    background-color: white;


}
</style>
