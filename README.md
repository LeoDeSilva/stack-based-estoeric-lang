# stack-based-estoeric-lang
a stack based esoteric language based loosely off of Element 

## Syntax
- <variable_name> - save top of stack to variable
- (variable_name) - load variable to top of stack
- ;0 - load number to top of stack
- , - remove value from top of stack
- . - print top of stack
- +,-,*,/ - mathematical operations, will add result to top of stack
  - will perform their operations on top of stack and the number following
    - if no number is following, 1 will be used instead
    - e.g. +10 will add 10 to the value at the top of the stack and add the result to the top of the stack
- : - string input
- \# - number input - if character is inputted, the ascii value will be stored
- ^ load top of stack 
- {repeat_times\ code } - for loop
  - ^ in place of repeat times will repeat as many times as the number on the top of the stack
  - ~ in place of repeat_times will repeat forever
- [condition\ code] - if block
  - e.g. [^=10\ .] 
    - if top of stack = 10 then print top of stack
 - @ - comment

## Example Program

### Truth Machine

```
# 
[ ^=1 \  @ if top of stack = 1
  { ~ \ @repeat forever
    . @ print
  }
]
```

### Count to 10

```
;0. @ load 0 onto stack and print
{ 10 \ @ repeat 10 times
  + . @ increment top of stack by 1 and print top of stack
}
```
### Calculator

```
#<n1> @ take in number input and store in n1
#<op> @ take in number input as operation, as operation is character, ascii value will be stored
#<n2> @ take in number input and store in n2

@ format is 1<n1> +<op> 2<n2>

(op) @ load operation to top of stack

[ ^=43 \ @ if top of stack (operation) = 43 (ascii value for +)
  (n1) @ load number 1 to top of stack
  +(n2) @ add number 2 to top of stack (number 1) and store result of top of stack
  . @ print top of stack (n1+n2)
]

[ ^=45 \ @ if top of stack (operation) = 45 (ascii value for -)
  (n1) @ load number 1 to top of stack
  -(n2) @ subtract number 2 from top of stack (number 1) and store result of top of stack
  . @ print top of stack (n1-n2)
]

[ ^=42 \ @ if top of stack (operation) = 42 (ascii value for *)
  (n1) @ load number 1 to top of stack
  *(n2) @ multiply top of stack by number 2 and store result of top of stack
  . @ print top of stack (n1*n2)
]

[ ^=47 \ @ if top of stack (operation) = 47 (ascii value for *)
  (n1) @ load number 1 to top of stack
  /(n2) @ divide  top of stack (number 1) by number 2 and store result of top of stack
  . @ print top of stack (n1/n2)
]


```


## TO DO
- implement less than or greater than as conditions
