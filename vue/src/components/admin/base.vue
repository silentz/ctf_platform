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
                <trainings-manager></trainings-manager>
            </tab>
            <tab name='Группы'>
                <group-manager></group-manager>
            </tab>
            <tab name='Категории'>
                <category-manager></category-manager>
            </tab>
        </tabs>
    </div>
</template>

<script>
import GroupManager from './groups.vue'
import NewsManager from './news.vue'
import ContestManager from './contests.vue'
import TrainingManager from './trainings.vue'
import CategoryManager from './categories.vue'

export default {
    name: 'AdminBase',
    components: {
        'group-manager': GroupManager,
        'news-manager': NewsManager,
        'contests-manager': ContestManager,
        'trainings-manager': TrainingManager,
        'category-manager': CategoryManager
    }
}
</script>

<style lang="scss">
@import '../../assets/style/tabs.scss';

.admin-panel {
    padding: 15px 0;

    .header {
        padding: 0 40px;
    }
}
</style>