<template>
    <div class='admin-panel'>
        <h2 class='header'>Администрирование</h2>
        <tabs>
            <tab name='Новости'>

            </tab>
            <tab name='Контесты'>

            </tab>
            <tab name='Тренировки'>

            </tab>
            <tab name='Группы'>

            </tab>
        </tabs>
    </div>
</template>

<script>

export default {
    name: 'AdminBase'
}
</script>

<style lang="scss">
@import '../../assets/style/tabs.scss';

.admin-panel {
    .header {
        padding: 0 40px;
    }
}
</style>