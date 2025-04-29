locals {
  entity_folders = fileset("${path.module}/../../entityTypes", "*")

  entities_data = [
    for folder in local.entity_folders : (
      {
        entity_info   = jsondecode(file("${path.module}/../../entityTypes/${folder}/${folder}.json"))
        entity_values = jsondecode(file("${path.module}/../../entityTypes/${folder}/entities/en.json"))
      }
    )
  ]

  entity_list = [
    for e in local.entities_data : {
      display_name            = e.entity_info.displayName
      kind                    = e.entity_info.kind
      enable_fuzzy_extraction = try(e.entity_info.enable_fuzzy_extraction, false)
      entities = [
        for ent in e.entity_values.entities : {
          value    = ent.value
          synonyms = ent.synonyms
        }
      ]
    }
  ]
}

resource "google_dialogflow_cx_entity_type" "basic_entity_type" {
  count        = length(local.entity_list)
  parent       = var.agent_id
  display_name = local.entity_list[count.index].display_name
  kind         = local.entity_list[count.index].kind

  dynamic "entities" {
    for_each = local.entity_list[count.index].entities
    content {
      value    = entities.value.value
      synonyms = entities.value.synonyms
    }
  }

  enable_fuzzy_extraction = local.entity_list[count.index].enable_fuzzy_extraction
}



locals {
  entity_json_files = fileset("${var.user_folder}/entityTypes", "**/*.json")

  entity_folders = [
    dirname(dirname(file))  # extracts 'branch' from 'entityTypes/branch/branch.json'
    for file in local.entity_json_files
    if file =~ ".*\\/entities\\/en\\.json"
  ]

  unique_folders = toset(local.entity_folders)

  entities_data = [
    for folder in local.unique_folders : {
      entity_info   = jsondecode(file("${var.user_folder}/entityTypes/${folder}/${folder}.json"))
      entity_values = jsondecode(file("${var.user_folder}/entityTypes/${folder}/entities/en.json"))
    }
  ]
