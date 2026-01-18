package me.schmot.qrcode

import com.google.zxing.BarcodeFormat
import com.google.zxing.client.j2se.MatrixToImageWriter
import com.google.zxing.qrcode.QRCodeWriter
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import java.io.ByteArrayOutputStream
import java.io.File
import java.nio.file.Files
import java.nio.file.Paths
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.*

@RestController
class QrController {

    @GetMapping("/health")
    fun health(): String {
        return "Service is running"
    }

    @GetMapping("/qr")
    fun qr(
        @RequestParam(required = false, defaultValue = "250") size: Int,
        @RequestParam(required = false, defaultValue = "png") type: String,
        @RequestParam(required = false, defaultValue = "") contents: String
    ): ResponseEntity<Any> {
        val validation = validateParams(size, type)
        if (validation != null) return validation

        return try {
            val imageBytes = generateQrCode(contents, size, type)
            ResponseEntity.ok()
                .contentType(getMediaType(type))
                .body(imageBytes)
        } catch (e: Exception) {
            ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error generating QR code: ${e.message}")
        }
    }

    @GetMapping("/qr/save")
    fun qrSave(
        @RequestParam(required = false, defaultValue = "250") size: Int,
        @RequestParam(required = false, defaultValue = "png") type: String,
        @RequestParam(required = false, defaultValue = "") contents: String
    ): ResponseEntity<Any> {
        val validation = validateParams(size, type)
        if (validation != null) return validation

        return try {
            val imageBytes = generateQrCode(contents, size, type)
            
            val directoryPath = Paths.get("/tmp/qr/")
            if (!Files.exists(directoryPath)) {
                Files.createDirectories(directoryPath)
            }

            val timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"))
            val uuid = UUID.randomUUID().toString().substring(0, 8)
            val extension = type.lowercase().let { if (it == "jpeg") "jpg" else it }
            val fileName = "qr_${timestamp}_${uuid}.$extension"
            val filePath = directoryPath.resolve(fileName)

            Files.write(filePath, imageBytes)

            ResponseEntity.ok()
                .contentType(MediaType.TEXT_PLAIN)
                .body("QR code saved successfully at: ${filePath.toAbsolutePath()}")
        } catch (e: Exception) {
            ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error saving QR code: ${e.message}")
        }
    }

    private fun validateParams(size: Int, type: String): ResponseEntity<Any>? {
        if (size !in 100..1000) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body("Size must be between 100 and 1000")
        }

        val lowerType = type.lowercase()
        if (lowerType != "png" && lowerType != "jpeg" && lowerType != "jpg") {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body("Only png and jpeg formats are supported")
        }
        return null
    }

    private fun getMediaType(type: String): MediaType {
        return when (type.lowercase()) {
            "png" -> MediaType.IMAGE_PNG
            else -> MediaType.IMAGE_JPEG
        }
    }

    private fun generateQrCode(contents: String, size: Int, type: String): ByteArray {
        val qrCodeWriter = QRCodeWriter()
        val qrContent = if (contents.isEmpty()) " " else contents
        val bitMatrix = qrCodeWriter.encode(qrContent, BarcodeFormat.QR_CODE, size, size)

        val baos = ByteArrayOutputStream()
        MatrixToImageWriter.writeToStream(bitMatrix, type.lowercase(), baos)
        return baos.toByteArray()
    }
}
