type QRS_DATA
        class_id
        r_peak
        r_peak_value
        rr_pre_interval
        rr_post_interval
        p_onset
        p_onset_val
        p_peak
        p_peak_val
        p_end
        p_end_val
        qrs_onset
        qrs_onset_val
        qrs_end
        qrs_end_val
        t_peak
        t_peak_val
        t_end
        t_end_val
end

QRS_DATA() = QRS_DATA(
  2,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null
  )
  
 QRS_DATA(data) = QRS_DATA(
  2,
  data[1],
  data[2],
  data[3],
  data[4],
  data[5],
  data[6],
  data[7],
  data[8],
  data[9],
  data[10],
  data[11],
  data[12],
  data[13],
  data[14],
  data[15],
  data[16],
  data[17],
  data[18],
  )