resource "google_dialogflow_cx_intent" "flight_booking_intent" {
  display_name = "FlightBookingIntent"
  location     = "us-central1"
  project      = "<YOUR_PROJECT_ID>"

  // 1. Book a flight
  training_phrases {
    repeat_count = 1
    parts {
      text = "Book a flight"
    }
  }

  // 2. Can you book my flight to San Francisco next month
  training_phrases {
    repeat_count = 1
    parts {
      text = "Can you book my flight to "
    }
    parts {
      text         = "San Francisco"
      parameter_id = "destination"
    }
    parts {
      text         = " next month"
      parameter_id = "travel_date"
    }
  }

  // 3. I want to use my reward points to book a flight from Milan in October
  training_phrases {
    repeat_count = 1
    parts {
      text = "I want to use my reward points to book a flight from "
    }
    parts {
      text         = "Milan"
      parameter_id = "origin"
    }
    parts {
      text = " in "
    }
    parts {
      text         = "October"
      parameter_id = "travel_date"
    }
  }

  // 4. My family is visiting next week and we need to book 6 round trip tickets
  training_phrases {
    repeat_count = 1
    parts {
      text = "My family is visiting next week and we need to book "
    }
    parts {
      text         = "6"
      parameter_id = "ticket_count"
    }
    parts {
      text = " round trip tickets"
    }
  }

  // 5. Four business class tickets from Taiwan to Dubai for June 2nd to 30th
  training_phrases {
    repeat_count = 1
    parts {
      text = "Four"
    }
    parts {
      text         = " business class"
      parameter_id = "travel_class"
    }
    parts {
      text = " tickets from "
    }
    parts {
      text         = "Taiwan"
      parameter_id = "origin"
    }
    parts {
      text = " to "
    }
    parts {
      text         = "Dubai"
      parameter_id = "destination"
    }
    parts {
      text = " for "
    }
    parts {
      text         = "June 2nd to 30th"
      parameter_id = "travel_date_range"
    }
  }

  // 6. I need a flight Saturday from LAX to San Jose (now without parameterizing "Saturday")
  training_phrases {
    repeat_count = 1
    parts {
      text = "I need a flight Saturday from "
    }
    parts {
      text         = "LAX"
      parameter_id = "origin"
    }
    parts {
      text = " to "
    }
    parts {
      text         = "San Jose"
      parameter_id = "destination"
    }
  }

  // 7. Book SFO to MIA on Au
