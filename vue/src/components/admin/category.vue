<template>
    <tr class='category-entry' v-if='exists'>
        <td class='name'>{{ category.name }}</td>
        <td>
            <button @click='$modal.show("edit-category" + category.id)'>&#9998;</button>
            <button @click='$modal.show("delete-category" + category.id)'>&#x2715;</button>
        </td>
        
        <modal :name='"delete-category" + category.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить категорию?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteCategory()">Да</button>
                    <button class='no' @click="$modal.hide('delete-category' + category.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-category" + category.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать категорию</h2>
                <form @submit.prevent="updateCategory">
                    <input size="40" v-model='name' placeholder="Название" required>
                    <button @click="$modal.hide('edit-category' + category.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>

<script>
import axios from 'axios'

export default {
    name: 'CategoryEntry',
    props: ['category'],
    data: function() {
        return {
            exists: true,
            name: this.category.name
        }
    },
    methods: {
        updateCategory() {
            axios.put(`/api/categories/${this.category.id}/`, {
                name: this.name
            }).then(response => {
                this.category.name = this.name
            })
        },
        deleteCategory() {
            axios.delete(`/api/categories/${this.category.id}/`).then(response => {
                this.exists = false
            })
        }
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/edit-wrapper.scss';
@import '../../assets/style/delete-wrapper.scss';
</style>