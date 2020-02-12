
js=$1

jsonnet \
-V reality=data \
-V engine=Pgrapher \
-V raw_input_label=tpcrawdecoder:daq \
-V sig_input_label=sig_input_label \
-V use_blob_reframer=use_blob_reframer \
-J cfg ${js}.jsonnet \
-o ${js}.json


wirecell-pgraph dotify --jpath -1 --no-params ${js}.json ${js}.pdf
#wirecell-pgraph dotify --jpath -1 ${js}.json ${js}.pdf
