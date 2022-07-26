## Python Implementation of tail -n k

### How to run
`python3 tail.py <filename> <number_of_lines>`

### How does it work?
1. It tries to a read some initial bytes from the given file
2. if the bytes to read is greater than file_length, reads the entire file
3. Else, read the bytes_to_read from end of file and count the number of line breaks
4. if the number of line breaks > n, we print the last n lines from those lines
5. Else if the number of line breaks < n, we update our count of bytes_to_read by a certain amount and follow from step 3 again