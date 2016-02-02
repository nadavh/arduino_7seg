int delay_time = 1;


// display sigments
int segments_num     = 8;
int segment_pins[]   = { 2, 3, 4, 5, 6, 7, 8, 9 };

// digits
int digits_num       = 4;
int digit_pins[]     = { 13, 12, 11, 10 };

int digit_vals[]     = { 0, 0, 0, 0 };

void setup()
{
  Serial.begin(9600);

  int digit;
  int segment;

  // define segment pins as output
  for (segment = 0; segment < segments_num; segment++)
    pinMode(segment_pins[segment], OUTPUT);      // set each pin as an output

  // define digit pins as output
  for (digit = 0; digit < digits_num; digit++)
    pinMode(digit_pins[digit], OUTPUT);      // set each pin as an output

  // nice load animation
  for (digit=0; digit  < digits_num; digit++)
  {
    digitalWrite(digit_pins[digit], HIGH);
    for (segment=0; segment < segments_num; segment++)
    {
      digitalWrite(segment_pins[segment], HIGH);
      delay(50);
      digitalWrite(segment_pins[segment], LOW);
    }

    digitalWrite(digit_pins[digit], LOW);
  }


}

// return  <base> in the power of <power>
int mypow(int base, int power)
{
  if(power == 0)
    return 1;

  return mypow(base,power-1)*base;
}

// refresh display
// must be called in a loop for consistent dfisplay
void refreshScreen()
{
  int digit;
  int segment;

  // go over digits
  for (digit=0; digit  < digits_num; digit++)
  {

    // go over segments
    for (segment=0; segment < segments_num; segment++)
    {
      // turn on/off required segments
      if (digit_vals[digit] & mypow(2,segment))
        digitalWrite(segment_pins[segment], HIGH);
      else
        digitalWrite(segment_pins[segment], LOW);
    }

    if (digit_vals[digit] > 0)
    {
      // display selected digit
      // (will light all previously selected sigments)
      // then stop, and go to the next digit.
      digitalWrite(digit_pins[digit], HIGH);
      delay(delay_time);
      digitalWrite(digit_pins[digit], LOW);
    }
    else
    {
        // don't bother in there is nothing to display
        delay(delay_time);
    }
  }
}

char incoming_data[]  = "0";
int  current_digit    = 0;
int  digit_value      = 0;
char input_char       = '0';
int  char_index       = 0;
int  tmp_value        = 0;
int temp_digit_vals[] = { 0, 0, 0, 0 };
void loop()
{

  if (Serial.available() > 0)
  {
    // read one byte from serial port
    incoming_data[0] = Serial.read();

    // if got to end sign
    if (incoming_data[0] == ';')
    {
      // clear unupdated digits in the end
      if (char_index > 0)
      {
        for (int digit=current_digit+1; digit < digits_num; digit++)
        {
          temp_digit_vals[digit] = 0;
        }
      }
      else
      {
        for (int digit=0; digit < digits_num; digit++)
        {
          temp_digit_vals[digit] = 0;
        }
      }
      // zero count
      char_index    = 0;
      current_digit = 0;
      digit_value   = 0;

      // update digit_vals
      for (int digit=0; digit < digits_num; digit++)
      {
        digit_vals[digit] = temp_digit_vals[digit];
      }
    }
    else
    {
      // det data
      sscanf(incoming_data,"%x", &tmp_value);
      if (char_index % 2 == 0)
      {
        digit_value = tmp_value*16;
        if (char_index != 0)
        {
          current_digit++;
        }
      }
      else
      {
        digit_value+= tmp_value;
      }
      char_index++;
      temp_digit_vals[current_digit] = digit_value;
    }
  }

  refreshScreen();
}
