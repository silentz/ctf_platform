<template>
    <div class='admin-panel'>
        <h2 class='header'>Администрирование</h2>
        <tabs>
            <tab name='Новости'>
                <news-manager></news-manager>
            </tab>
            <tab name='Контесты'>
                <contests-manager></contests-manager>
            </tab>
            <tab name='Тренировки'>

            </tab>
            <tab name='Группы'>
                <group-manager></group-manager>
            </tab>
        </tabs>
    </div>
</template>

<script>
import GroupManager from './groups.vue'
import NewsManager from './news.vue'
import ContestManager from './contests.vue'

export default {
    name: 'AdminBase',
    components: {
        'group-manager': GroupManager,
        'news-manager': NewsManager,
        'contests-manager': ContestManager
    }
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