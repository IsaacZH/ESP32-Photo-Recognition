#include <esp_log.h>
#include <esp_system.h>
#include <nvs_flash.h>
#include <sys/param.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// support IDF 5.x
#ifndef portTICK_RATE_MS
#define portTICK_RATE_MS portTICK_PERIOD_MS
#endif

#include "esp_camera.h"
#include "wifi_sta.h"

#define CAM_PIN_PWDN 32
#define CAM_PIN_RESET -1 //software reset will be performed
#define CAM_PIN_XCLK 0
#define CAM_PIN_SIOD 26
#define CAM_PIN_SIOC 27

#define CAM_PIN_D7 35
#define CAM_PIN_D6 34
#define CAM_PIN_D5 39
#define CAM_PIN_D4 36
#define CAM_PIN_D3 21
#define CAM_PIN_D2 19
#define CAM_PIN_D1 18
#define CAM_PIN_D0 5
#define CAM_PIN_VSYNC 25
#define CAM_PIN_HREF 23
#define CAM_PIN_PCLK 22

// #define BLINK_GPIO 4
#define EN_POST_IMAGE

static const char *TAG = "take_picture";

#if ESP_CAMERA_SUPPORTED
static camera_config_t camera_config = {
    .pin_pwdn = CAM_PIN_PWDN,
    .pin_reset = CAM_PIN_RESET,
    .pin_xclk = CAM_PIN_XCLK,
    .pin_sccb_sda = CAM_PIN_SIOD,
    .pin_sccb_scl = CAM_PIN_SIOC,

    .pin_d7 = CAM_PIN_D7,
    .pin_d6 = CAM_PIN_D6,
    .pin_d5 = CAM_PIN_D5,
    .pin_d4 = CAM_PIN_D4,
    .pin_d3 = CAM_PIN_D3,
    .pin_d2 = CAM_PIN_D2,
    .pin_d1 = CAM_PIN_D1,
    .pin_d0 = CAM_PIN_D0,
    .pin_vsync = CAM_PIN_VSYNC,
    .pin_href = CAM_PIN_HREF,
    .pin_pclk = CAM_PIN_PCLK,

    //XCLK 20MHz or 10MHz for OV2640 double FPS (Experimental)
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,

    .pixel_format = PIXFORMAT_JPEG, //YUV422,GRAYSCALE,RGB565,JPEG
    .frame_size = FRAMESIZE_QXGA,    //QQVGA-UXGA, For ESP32, do not use sizes above QVGA when not JPEG. The performance of the ESP32-S series has improved a lot, but JPEG mode always gives better frame rates.

    .jpeg_quality = 3, //0-63, for OV series camera sensors, lower number means higher quality
    .fb_count = 5,       //When jpeg mode is used, if fb_count more than one, the driver will work in continuous mode.
    .fb_location = CAMERA_FB_IN_PSRAM,
    .grab_mode = CAMERA_GRAB_WHEN_EMPTY,
};

static esp_err_t init_camera(void)
{
    //initialize the camera
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK)
    {
        ESP_LOGE(TAG, "Camera Init Failed");
        return err;
    }

    return ESP_OK;
}
#endif

#ifdef BLINK_GPIO
#include "driver/gpio.h"

static void flash_led_task(void *pvParameters)
{
    /* Set the GPIO level according to the state (LOW or HIGH)*/
    gpio_set_level(BLINK_GPIO, 1);
    ESP_LOGI(TAG, "Turning the LED ON");
    vTaskDelay(500 / portTICK_RATE_MS);   
    gpio_set_level(BLINK_GPIO, 0);
    ESP_LOGI(TAG, "Turning the LED OFF");
    vTaskDelete(NULL);
}

static void led_init(void)
{
    ESP_LOGI(TAG, "configured to blink GPIO LED!");
    gpio_reset_pin(BLINK_GPIO);
    /* Set the GPIO as a push/pull output */
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);
}
#endif

void app_main(void)
{
    // Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    #ifdef EN_POST_IMAGE
    wifi_init_sta();
    #endif
    #ifdef BLINK_GPIO
    led_init();
    #endif
#if ESP_CAMERA_SUPPORTED
    if(ESP_OK != init_camera()) {
        return;
    }
    for (int i = 0; i < 10; i++)
    {
        ESP_LOGI(TAG, "Taking picture...");
        #ifdef BLINK_GPIO
        xTaskCreate(&flash_led_task, "flash_led_task", 4096, NULL, 5, NULL);
        #endif
        camera_fb_t *pic = esp_camera_fb_get();
        // LOG size, format, height and width
        ESP_LOGI(TAG, "Picture taken! Size: %zu bytes, Format: %d, Width: %d, Height: %d", pic->len, pic->format, pic->width, pic->height);
        ESP_LOG_BUFFER_HEX(TAG, pic->buf, MIN(32, pic->len));
        #ifdef EN_POST_IMAGE
        // http_post((const char *)pic->buf, pic->len);
        #endif
        
        vTaskDelay(1 / portTICK_RATE_MS);
        if (i % camera_config.fb_count == 0)
        {
            ESP_LOGI(TAG, "esp_camera_return_all");
            esp_camera_return_all();
        }
    }
    
#else
    ESP_LOGE(TAG, "Camera support is not available for this chip");
    return;
#endif
}
