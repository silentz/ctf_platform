<template lang="html">
    <div class="ctf-platform">
        <div class="ctf-sidebar">
            <h3 class='ctf-sidebar-username'>{{ username }}</h3>
            <hr class='ctf-sidebar-delimiter'>
            <ul class='ctf-sidebar-list'>
                <li class='ctf-sidebar-list-item'>Новости</li>
                <li class='ctf-sidebar-list-item'>Тренировки</li>
                <li class='ctf-sidebar-list-item'>Контесты</li>
                <li class='ctf-sidebar-list-item'>Личный кабинет</li>
                <li class='ctf-sidebar-list-item'>Группы</li>
                <li class='ctf-sidebar-list-item'>Скорборд</li>
            </ul>
        </div>
        <div class="ctf-screen">
            <div class="ctf-contest-item">
                <div class='ctf-contest-item-data'>
                    <h3 class='ctf-contest-item-label'>Тренировка на хеши</h3>
                    <p class='ctf-contest-item-time'>
                        &#128336; c 15:00 10.10.2010 до 16:00 11.11.2011
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Platfrom',
    computed: {
        username: function() {
            return this.$store.state.username;
        }
    }
}
</script>

<style lang="css">
</style>
