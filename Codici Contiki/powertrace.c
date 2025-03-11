/*
 * Copyright (c) 2007, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

/**
 * \file
 *         Demonstrating the powertrace application with broadcasts
 * \author
 *         Adam Dunkels <adam@sics.se>
 */

#include "contiki.h"          // Include the Contiki operating system header file
#include "net/rime.h"         // Include the Rime network stack header file
#include "random.h"           // Include the random number generator header file
#include "powertrace.h"       // Include the powertrace application header file
#include "dev/button-sensor.h" // Include the button sensor device driver header file
#include "dev/leds.h"         // Include the LEDs device driver header file
#include <stdio.h>            // Include the standard input-output header file
/*---------------------------------------------------------------------------*/
PROCESS(example_broadcast_process, "BROADCAST example"); // Declare a process called "example_broadcast_process"
AUTOSTART_PROCESSES(&example_broadcast_process);         // Automatically start the "example_broadcast_process"
/*---------------------------------------------------------------------------*/
static void broadcast_recv(struct broadcast_conn *c, const rimeaddr_t *from) {
  // Define a callback function to handle received broadcast messages
  printf("broadcast message received from %d.%d: '%s'\n",
         from->u8[0], from->u8[1], (char *)packetbuf_dataptr());
  // Print the sender's address and the received message
}

static const struct broadcast_callbacks broadcast_call = {broadcast_recv};
// Define a structure containing the callback function for broadcast communication

static struct broadcast_conn broadcast; 
// Declare a broadcast connection
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(example_broadcast_process, ev, data) {
  static struct etimer et; // Declare an event timer

  PROCESS_EXITHANDLER(broadcast_close(&broadcast);) 
  // Ensure that the broadcast connection is closed when the process exits

  PROCESS_BEGIN(); // Begin the process

  powertrace_start(CLOCK_SECOND * 2); 
  // Start power tracing, with an interval of two seconds

  broadcast_open(&broadcast, 129, &broadcast_call); 
  // Open the broadcast connection on channel 129 with the specified callback

  while(1) { // Infinite loop
    etimer_set(&et, CLOCK_SECOND * 4 + random_rand() % (CLOCK_SECOND * 4)); 
    // Set the event timer with a delay between 4 and 8 seconds

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et)); 
    // Wait for the event timer to expire

    packetbuf_copyfrom("Hello", 6); 
    // Copy the message "Hello" into the packet buffer

    broadcast_send(&broadcast); 
    // Send the broadcast message

    printf("broadcast message sent\n"); 
    // Print a confirmation message
  }

  PROCESS_END(); 
  // End the process
}
/*---------------------------------------------------------------------------*/
