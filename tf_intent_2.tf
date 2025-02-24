resource "google_dialogflow_cx_intent" "flight_booking_intent" {
  display_name = "FlightBookingIntent"
  location     = "us-central1"          # Adjust as needed
  project      = "<YOUR_PROJECT_ID>"    # Replace with your project ID

  // Training phrases with annotated parts:
  training_phrases {
    repeat_count = 1
    parts {
      text = "Book a flight"
    }
  }

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

  training_phrases {
    repeat_count = 1
    parts {
      text = "I need a flight "
    }
    parts {
      text         = "Saturday"
      parameter_id = "travel_day"
    }
    parts {
      text = " from "
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

  training_phrases {
    repeat_count = 1
    parts {
      text = "Book "
    }
    parts {
      text         = "SFO"
      parameter_id = "origin"
    }
    parts {
      text = " to "
    }
    parts {
      text         = "MIA"
      parameter_id = "destination"
    }
    parts {
      text = " on "
    }
    parts {
      text         = "August 10th"
      parameter_id = "travel_date"
    }
    parts {
      text         = " one way"
      parameter_id = "flight_type"
    }
  }

  training_phrases {
    repeat_count = 1
    parts {
      text = "Help me book a ticket from "
    }
    parts {
      text         = "4/10"
      parameter_id = "start_date"
    }
    parts {
      text = " to "
    }
    parts {
      text         = "4/15"
      parameter_id = "end_date"
    }
    parts {
      text = " from "
    }
    parts {
      text         = "Mexico City"
      parameter_id = "origin"
    }
    parts {
      text = " to "
    }
    parts {
      text         = "Medellin Colombia"
      parameter_id = "destination"
    }
    parts {
      text = " please"
    }
  }

  training_phrases {
    repeat_count = 1
    parts {
      text = "I am booking a surprise trip for my mom, can you help arrange that for "
    }
    parts {
      text         = "May 10th to May 25th"
      parameter_id = "travel_date_range"
    }
    parts {
      text = " to "
    }
    parts {
      text         = "Costa Rica"
      parameter_id = "destination"
    }
  }

  training_phrases {
    repeat_count = 1
    parts {
      text = "Do you have any cheap flights to "
    }
    parts {
      text         = "NYC"
      parameter_id = "destination"
    }
    parts {
      text = " for "
    }
    parts {
      text         = "this weekend"
      parameter_id = "travel_date"
    }
  }

  training_phrases {
    repeat_count = 1
    parts {
      text = "I want to fly in my cousin from "
    }
    parts {
      text         = "Montreal"
      parameter_id = "origin"
    }
    parts {
      text = " on "
    }
    parts {
      text         = "August 8th"
      parameter_id = "travel_date"
    }
  }

  training_phrases {
    repeat_count = 1
    parts {
      text = "I want to find "
    }
    parts {
      text         = "two"
      parameter_id = "ticket_count"
    }
    parts {
      text = " seats to "
    }
    parts {
      text         = "Panama City"
      parameter_id = "destination"
    }
    parts {
      text = " on "
    }
    parts {
      text         = "July 4th"
      parameter_id = "travel_date"
    }
  }

  training_phrases {
    repeat_count = 1
    parts {
      text = "For my wedding anniversary we want to go to "
    }
    parts {
      text         = "Seattle"
      parameter_id = "destination"
    }
    parts {
      text = " for "
    }
    parts {
      text         = "Christmas"
      parameter_id = "travel_date"
    }
  }

  // Parameter definitions required by the training phrases:
  parameter {
    id          = "destination"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.geo-city"
  }

  parameter {
    id          = "travel_date"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.date"
  }

  parameter {
    id          = "origin"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.geo-city"
  }

  parameter {
    id          = "ticket_count"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.number"
  }

  parameter {
    id          = "travel_class"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.any"
  }

  parameter {
    id          = "travel_day"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.day-of-week"
  }

  parameter {
    id          = "travel_date_range"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.date-period"
  }

  parameter {
    id          = "flight_type"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.any"
  }

  parameter {
    id          = "start_date"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.date"
  }

  parameter {
    id          = "end_date"
    entity_type = "projects/<YOUR_PROJECT_ID>/locations/us-central1/agents/<YOUR_AGENT_ID>/entityTypes/@sys.date"
  }
}
