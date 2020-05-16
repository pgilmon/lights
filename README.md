Note: This is not an official Google product and
it's not supported by Google in any way.

This is not a Shelly.cloud product and it's not
supported by Shelly.cloud in any way.

Lights is an automation framework for smart switches or lights.

It was initially developed to work with shelly.cloud devices, but
could potentially work with any other devices that support
webhooks and provide an API to send commands to the devices.

# Applications

# Set-up

Instructions to set-up the solution on Google Cloud Functions follows.
It hould be possible to deploy on other platforms or on your own
computer (in this case, you'd need to keep it powered up for it to work).

## 1. Create configuration spreadsheet

Configuration is stored on a Google Spreadsheet. The Spredsheet must
contain the following columns:

| Name | External ID | Internal ID | Channel | Mode | Start time | End time | Timer |
|------|-------------|-------------|---------|------|------------|----------|-------|
|      |             |             |         |      |            |          |       |
|      |             |             |         |      |            |          |       |
|      |             |             |         |      |            |          |       |

Here is a description of what each column means:

 * **Name** This is for you to identify the element this row
   refers to. You can input any value here.
 * **External ID** ID that identifies the device on the Firestore database.
 * **Internal ID** ID that identifies the device on the Shelly API.
 * **Channel** Device's channel. This is used to identify the device
   with the Shelly API, as several devices might have the same ID and
   different channels.
 * **Mode** Mode for the device. The following modes are currently
   supported:
    * *scheduled_timer* The device will be automatically shut off after
      X minutes, which are defined in the column *Timer*.
 * **Start time** The rule will only be active between *Start time*
   and *End time*
 * **End time** The rule will only be active between *Start time*
   and *End time*
 * **Timer** For timers, number of minutes.
