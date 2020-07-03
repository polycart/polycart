# myuart 协议
## K210 UART
- 商品数据传输: json 数据, 格式如下. 数据以 `b'\r\n'` 结尾 
```json
[
  {
    "code": "code_of_products_in_str",
    "count": number_of_products_in_int
  },
  {
    "code": ...,
    "count": ...
  },
  ... 
]
```
- 树莓派发送的获取数据指令: `b'GET\r\n'`
- 在树莓派发出请求后, K210 应在 500ms 内返回 `b'OK\r\n'` 的 OK 信号. 若未返回, 可判定超时
- 在 K210 发出 OK 信号后, 进行商品数据回传, 回传时间不限.
