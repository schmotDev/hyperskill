package me.schmot.qrcode

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class QrApplication

fun main(args: Array<String>) {
    runApplication<QrApplication>(*args)
}
