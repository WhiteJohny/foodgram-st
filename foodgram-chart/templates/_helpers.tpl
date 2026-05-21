{{/*
Expand the name of the chart.
*/}}
{{- define "foodgram.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "foodgram.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "foodgram.backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "foodgram.name" . }}-backend
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Nginx selector labels
*/}}
{{- define "foodgram.nginx.selectorLabels" -}}
app.kubernetes.io/name: {{ include "foodgram.name" . }}-nginx
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Namespace
*/}}
{{- define "foodgram.namespace" -}}
{{- .Values.namespace }}
{{- end }}

{{/*
Name of the K8s Secret created by ESO
*/}}
{{- define "foodgram.secretName" -}}
{{- .Values.externalSecrets.secretName }}
{{- end }}
