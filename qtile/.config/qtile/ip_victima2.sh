#!/bin/bash

# Comprueba si la variable victim está definida
if [ -n "$victim" ]; then
    # Imprime el valor de la variable victim si está definida
    echo "$victim"
else
    # Imprime "No Victim" si la variable no está definida
    echo "No Victim"
fi
