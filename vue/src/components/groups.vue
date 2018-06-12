<template>
	<div class='groups'>
		<h2>Группы</h2>
		<group v-for='group in groups' :key='group.id' :group="group"></group>
	</div>	
</template>

<script>
import axios from 'axios'
import GroupComponent from './group.vue'

export default {
	name: 'Groups',
	data: function() {
		return {
			groups: []
		}
	},
	created: function() {
		axios.get('/api/groups/').then(response => {
			this.groups = response.data
		})
	},
	components: {
		group: GroupComponent
	}
}
</script>

<style lang="scss">

.groups {
	padding: 10px 30px;
}

</style>