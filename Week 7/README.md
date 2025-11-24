# Project for module CST1510

# Week 7: Secure Authentication System

Student Name: Abdelkerim Mahamat Habib Doutoum

Student ID: [M01095127]

Course: CST1510-CW2- MULTI-DOMAIN Intelligence Platform

## Project Description

A command-line authentication program that implements secure password hashing. The authentication system permits users to register accounts and log in with proper pass

## Features

-Secure password hashing using bcrypt with automatic salt generation

-User registration with duplicate username prevention

-User login with password verification

-Input validation for usernames and passwords

-File-based user data persistence

## Technical Implementation

-Hashing Algorithm: bcrypt with automatic salting

-Data Storage: Plain text file ('users.txt') with comma-seperated values

-password Security: One-way hashing, no plaintext storage.

-Validation: Username (3-25 alphanumeric characters), Password(5-50 characters)

