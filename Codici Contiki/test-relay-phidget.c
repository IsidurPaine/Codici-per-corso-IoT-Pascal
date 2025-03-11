/*
 * Copyright (c) 2011, Zolertia(TM) is a trademark of Advancare,SL
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
 *         A quick program for testing a generic relay device connected in the
 *         phidget port
 * \author
 *         Antonio Lignan <alinan@zolertia.com>
 * working directory: ~/contiki-2.7/examples/z1
 */

#include <stdio.h>                     // Include standard input-output library
#include "contiki.h"                   // Include Contiki operating system library
#include "dev/relay-phidget.h"         // Include relay phidget device driver library

#if 1
#define PRINTF(...) printf(__VA_ARGS__)   // Define PRINTF to print output if condition is true
#else
#define PRINTF(...)                       // Define PRINTF to do nothing if condition is false
#endif

#if 0
#define PRINTFDEBUG(...) printf(__VA_ARGS__) // Define PRINTFDEBUG to print debug output if condition is true
#else
#define PRINTFDEBUG(...)                    // Define PRINTFDEBUG to do nothing if condition is false
#endif

#define RELAY_INTERVAL (CLOCK_SECOND)   // Define the interval for relay toggling as one second

PROCESS(test_process, "Relay test process"); // Declare the main process with a descriptive name
AUTOSTART_PROCESSES(&test_process);          // Automatically start the main process

/*---------------------------------------------------------------------------*/
static struct etimer et;              // Declare an event timer
static uint8_t status;                // Declare a variable to store the relay status

PROCESS_THREAD(test_process, ev, data)
{
  PROCESS_BEGIN();                     // Start of the process

  relay_enable(7);                     // Enable the relay control on pin P6.7

  while(1) {                           // Infinite loop
    etimer_set(&et, RELAY_INTERVAL);   // Set the event timer to the defined interval
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et)); // Wait until the timer expires
    
    status = relay_toggle();           // Toggle the relay status (ON/OFF)
    PRINTF("Relay [%d]\n", status);    // Print the current status of the relay
  }
  
  PROCESS_END();                       // End of the process
}
