# Wait for the SFT job to finish
wait_for_completion(sft_tuning_job)

# Always refresh to get latest state after wait
sft_tuning_job.refresh()
final_state = sft_tuning_job.state.name
print(f"SFT job ended with state: {final_state}")

if final_state == "JOB_STATE_SUCCEEDED":
    print(f"HARNESS_EXPORT_SFT_RESOURCE_NAME={sft_tuning_job.resource_name}")
    return sft_tuning_job.resource_name

elif final_state == "JOB_STATE_FAILED":
    raise RuntimeError("SFT Job Failed")

else:
    raise RuntimeError(f"SFT Job ended in unexpected state: {final_state}")
