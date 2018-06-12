<template>
	<div class='group'>
		<div class='header'>{{ group.name }}</div>
		<template v-if='group.inside'>
			<p class='already-inside'>Вы состоите в этой группе</p>
		</template>
		<template v-else>
			<form @submit.prevent="enterGroup()">
				<input size="25" v-model='invite_code' type='password' placeholder='Инвайт-код'>
				<button class="enter-button">Вступить</button>
			</form>
		</template>
	</div>
</template>

<script>
import axios from 'axios'

export default {
	name: "Group",
	props: ['group'],
	data: function() {
		return {
			invite_code: "",
			showStatus: false,
			status: ""
		}
	},
	methods: {
		enterGroup() {
			axios.post(`/api/groups/${this.group.id}/access/`, {"invite_code": this.invite_code})
			.then(response => {
				this.group.inside = true
			})
		}
	}
}
</script>

<style lang="scss">
.group {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	background-color: white;
	padding: 10px;
	border-radius: 5px;
	margin: 10px 0;

	.header {
		display: inline-block;
		margin: 0 5px;
	}

	.already-inside {
		margin: 6px;
	}

	form {
		margin: 0 5px;

		button {
			display: inline-block;
			outline: none;
			user-select: none;
			border: none;
			background-color: lightgreen;
			padding: 7px;
			border-radius: 5px;
		}
		input {
			padding: 6px;
			border-radius: 5px;
			border: none;
			background-color: #ffe4b5;
			outline: none;
		}
	}
}
</style>