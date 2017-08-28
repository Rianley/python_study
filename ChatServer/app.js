var io = require('socket.io').listen(3000)
io.on('connection', function (socket) {
	console.log("客户端连接成功!")
	socket.on('send', function (data) {
		socket.broadcast.emit('receive', { "user": socket.id, "data": data })
	})
})