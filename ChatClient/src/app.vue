<template>
	<div id="app">
		<f7-statusbar></f7-statusbar>
		<f7-views>
			<f7-view id="main-view" navbar-through :dynamic-navbar="true" main>
				<f7-navbar v-if="$theme.ios">
					<f7-nav-center sliding>ceshuChat客户端</f7-nav-center>
					</f7-nav-right>
				</f7-navbar>
				<f7-pages>
					<f7-page>

						<f7-messages>
							<f7-message v-for="message in messages" :text="message.text" :date="message.date" :name="message.name" :avatar="message.avatar" :type="message.type" :day="message.day" :time="message.time">
							</f7-message>
						</f7-messages>
						<f7-messagebar placeholder="请输入..." send-link="发送" @submit="onSubmit"></f7-messagebar>

					</f7-page>
				</f7-pages>
			</f7-view>
		</f7-views>

	</div>
</template>

<script>
	export default {
		data: function() {
			return {
				messages: []
			}
		},
		sockets: {
			connect: function() {},
			customEmit: function(val) {}
		},
		created() {
			this.$options.sockets.receive = (content) => {
				this.messages.push({
					name: content.user,
					avatar:content.data.avatar,
					text: content.data.text,
					date: content.data.sendDate,
					type: 'received',
				})
			}
		},
		methods: {
			onSubmit: function(text, clear) {
				if(text.trim().length === 0) return
				let sendDate = (function() {
					let now = new Date();
					let hours = now.getHours();
					let minutes = now.getMinutes()
					let seconds = now.getSeconds();
					return hours + ':' + minutes + ':' + seconds
				})()
				let avatar = require('./img/avatar.png')
				let sendEmit = {
					"text": text,
					"avatar": avatar,
					"sendDate": sendDate,
				}
				this.$socket.emit('send', sendEmit)
				this.messages.push({
					avatar: avatar,
					text: text,
					date: sendDate
				})
				clear()
			}
		}
	}
</script>
<style>

</style>