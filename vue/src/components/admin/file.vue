<template>
    <tr class='file-entry' v-if='exists'>
        <td>{{ file.name }}</td>
        <td>
            <button @click='$modal.show("delete-file" + file.id)'>&#x2715;</button>
        </td>
        <modal :name='"delete-file" + file.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить файл?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteFile()">Да</button>
                    <button class='no' @click="$modal.hide('delete-file' + file.id)">Нет</button>
                </div>
            </div>
        </modal>
    </tr>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AdminFileEdit',
    props: ['file'],
    data: function() {
        return {
            exists: true
        }
    },
    methods: {
        deleteFile() {
            axios.delete(`/api/files/${this.file.id}/`).then(response => {
                this.exists = false
            })
        }
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/delete-wrapper.scss'; 
</style>