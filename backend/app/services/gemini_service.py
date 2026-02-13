"""
Serviço de integração com Google Gemini 2.5 Pro para geração de relatórios médicos.

Implementa comunicação com a API Gemini para análise multimodal de vídeos e áudios,
geração de laudos técnicos e descrição contextualizada de anomalias.
"""

import asyncio
import base64
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import google.generativeai as genai

from app.core.config import settings
from app.core.logging_config import get_logger
from app.models.schemas import VideoAnalysisResult, AudioAnalysisResult

logger = get_logger(__name__)


class GeminiService:
    """
    Serviço para geração de relatórios médicos usando Gemini 2.5 Pro.
    
    Capabilities:
    - Análise multimodal (texto + vídeo frames)
    - Geração de laudos técnicos estruturados
    - Transcrição e análise de áudio
    - Retry automático com backoff exponencial
    
    Attributes:
        model: Instância do modelo Gemini configurada.
    """
    
    def __init__(self):
        """Inicializa o serviço Gemini com a API key configurada."""
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            logger.info(f"Gemini Service inicializado com modelo: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"Erro ao inicializar Gemini Service: {e}")
            raise RuntimeError(f"Falha na inicialização do Gemini: {e}")
    
    async def generate_video_report(self, analysis_result: VideoAnalysisResult) -> str:
        """
        Gera relatório médico técnico a partir da análise de vídeo cirúrgico.
        
        O relatório é estruturado em seções: Sumário Executivo, Achados por Categoria,
        Momentos Críticos, Recomendações e Limitações da Análise Automatizada.
        
        Args:
            analysis_result: Resultado completo da análise de vídeo.
        
        Returns:
            Relatório em formato Markdown com análise clínica.
        """
        try:
            logger.info(f"Construindo prompt para análise de vídeo {analysis_result.analysis_id}")
            prompt = self._build_video_prompt(analysis_result)
            logger.info(f"Prompt construído com {len(prompt)} caracteres. Chamando Gemini API...")
            logger.info(f"Modelo Gemini em uso: {settings.GEMINI_MODEL}")
            
            report = await self._generate_with_retry(prompt)
            logger.info(f"✅ Relatório de vídeo gerado com sucesso: {len(report)} caracteres")
            return report
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO ao gerar relatório de vídeo: {type(e).__name__}: {e}", exc_info=True)
            logger.warning(f"Gerando relatório fallback para análise {analysis_result.analysis_id}")
            return self._generate_fallback_video_report(analysis_result)
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcreve áudio para texto usando Gemini File API.
        
        Args:
            audio_file_path: Caminho do arquivo de áudio.
        
        Returns:
            Transcrição completa do áudio em português brasileiro.
        """
        try:
            logger.info(f"Iniciando transcrição de áudio: {audio_file_path}")
            
            # Upload do arquivo para Gemini
            audio_path = Path(audio_file_path)
            logger.info(f"Fazendo upload do arquivo para Gemini API...")
            audio_file = genai.upload_file(path=str(audio_path))
            logger.info(f"Arquivo uploaded: {audio_file.uri}")
            
            # Prompt para transcrição
            prompt = """
            Faça a transcrição COMPLETA E FIEL deste áudio em português brasileiro.
            
            IMPORTANTE:
            - Transcreva PALAVRA POR PALAVRA tudo que é dito no áudio
            - Mantenha a ordem exata das falas
            - Inclua hesitações, pausas longas e repetições se houver
            - Use pontuação adequada (vírgulas, pontos, interrogações)
            - Separe em parágrafos quando houver mudança de assunto
            - Se houver múltiplos falantes, identifique cada um
            - Se algo não for compreensível, use [inaudível]
            
            Retorne APENAS a transcrição, sem comentários adicionais.
            """
            
            # Gera transcrição
            logger.info("Chamando Gemini para transcrever...")
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, audio_file]
            )
            
            transcription = response.text.strip()
            logger.info(f"✅ Transcrição gerada com sucesso: {len(transcription)} caracteres")
            
            # Deleta arquivo temporário do Gemini
            try:
                genai.delete_file(audio_file.name)
                logger.info("Arquivo temporário removido do Gemini")
            except Exception as e:
                logger.warning(f"Não foi possível deletar arquivo temporário: {e}")
            
            return transcription
        
        except Exception as e:
            logger.error(f"❌ Erro ao transcrever áudio: {e}", exc_info=True)
            return "[Transcrição não disponível - erro ao processar áudio]"
    
    async def generate_audio_report(self, analysis_result: AudioAnalysisResult) -> str:
        """
        Gera relatório psicológico a partir da análise de áudio de consulta.
        
        Seções: Perfil Vocal, Indicadores Psicológicos, Momentos de Risco,
        Recomendações e Disclaimer.
        
        Args:
            analysis_result: Resultado completo da análise de áudio.
        
        Returns:
            Relatório em formato Markdown com análise psicológica.
        """
        try:
            logger.info(f"Construindo prompt para análise de áudio {analysis_result.analysis_id}")
            prompt = self._build_audio_prompt(analysis_result)
            logger.info(f"Prompt construído com {len(prompt)} caracteres. Chamando Gemini API...")
            
            report = await self._generate_with_retry(prompt)
            logger.info(f"Relatório de áudio gerado com sucesso: {len(report)} caracteres")
            return report
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de áudio: {e}", exc_info=True)
            logger.warning(f"Gerando relatório fallback para análise {analysis_result.analysis_id}")
            return self._generate_fallback_audio_report(analysis_result)
    
    async def analyze_frame_description(self, frame_b64: str, context: str) -> str:
        """
        Analisa um frame específico usando Gemini Vision.
        
        Args:
            frame_b64: Frame codificado em base64 (JPEG).
            context: Contexto clínico adicional para a análise.
        
        Returns:
            Descrição detalhada das anomalias visíveis no frame.
        """
        prompt = f"""
Você é um especialista em análise de imagens médicas ginecológicas.

Contexto: {context}

Analise a imagem cirúrgica fornecida e descreva:
1. Estruturas anatômicas visíveis
2. Instrumentos cirúrgicos identificados
3. Anomalias ou áreas de preocupação
4. Qualidade da visualização

Seja objetivo e técnico. Limite a resposta a 150 palavras.
"""
        
        try:
            # Decodifica base64 para criar a imagem
            image_bytes = base64.b64decode(frame_b64)
            
            # Gemini Vision API
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, {"mime_type": "image/jpeg", "data": image_bytes}]
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Erro na análise de frame com Gemini Vision: {e}")
            return "Análise de frame indisponível no momento."
    
    def _build_video_prompt(self, analysis_result: VideoAnalysisResult) -> str:
        """
        Constrói o prompt estruturado para geração de relatório de vídeo.
        
        Args:
            analysis_result: Dados da análise de vídeo.
        
        Returns:
            Prompt formatado para o Gemini.
        """
        # Calcula estatísticas
        total_anomalies = sum(analysis_result.anomaly_summary.values())
        critical_frames = [
            f for f in analysis_result.frames 
            if f.severity == "critical"
        ]
        high_severity_frames = [
            f for f in analysis_result.frames 
            if f.severity == "high"
        ]
        
        # Identifica momentos críticos (timestamps)
        critical_moments = [
            f"{f.timestamp_seconds:.1f}s" 
            for f in critical_frames[:5]  # Top 5
        ]
        
        # Coleta informações detalhadas dos instrumentos detectados
        instruments_info = self._extract_instruments_info(analysis_result)
        
        prompt = f"""
Você é um especialista em análise de procedimentos cirúrgicos ginecológicos assistido por inteligência artificial.

**DADOS DA ANÁLISE**

- Arquivo: {analysis_result.filename}
- Duração: {analysis_result.duration_seconds:.1f} segundos
- Frames analisados: {analysis_result.total_frames_analyzed}
- Total de anomalias detectadas: {total_anomalies}

**SUMÁRIO DE ANOMALIAS POR TIPO**
{self._format_anomaly_summary(analysis_result.anomaly_summary)}

**DISTRIBUIÇÃO DE SEVERIDADE**
- Frames críticos: {len(critical_frames)}
- Frames de alta severidade: {len(high_severity_frames)}
- Frames de média severidade: {len([f for f in analysis_result.frames if f.severity == "medium"])}

**MOMENTOS CRÍTICOS IDENTIFICADOS**
Timestamps com severidade crítica: {', '.join(critical_moments) if critical_moments else 'Nenhum'}

{instruments_info}

---

**TAREFA**

Gere um laudo médico técnico DETALHADO em português (pt-BR) seguindo a estrutura:

## 📋 Sumário Executivo
[Parágrafo conciso sobre o procedimento analisado, duração, e principais achados quantitativos]

## 🔍 Achados Detalhados

### 🩸 Sangramento e Hemostasia
- Descreva a presença, intensidade e localização de sangramento detectado
- Avalie a adequação da hemostasia durante o procedimento
- Identifique momentos de sangramento excessivo (com timestamps)

### 🔧 Instrumentação Cirúrgica
- **Liste ESPECIFICAMENTE** cada instrumento detectado (ex: pinça de Babcock, tesoura de Metzenbaum, trocarte, aspirador, bisturi elétrico)
- Comente sobre o uso apropriado e técnica de manuseio
- Identifique instrumentos que aparecem em momentos críticos
- Avalie a ergonomia e coordenação dos movimentos

### ⚠️ Anomalias e Eventos Adversos
- Detalhe cada tipo de anomalia detectada
- Para "Instrument Detected": especifique qual instrumento e contexto
- Descreva movimentos anormais, tremores ou hesitações
- Avalie obstruções de campo visual ou problemas de iluminação

### 📍 Anatomia e Campo Cirúrgico
- Identifique estruturas anatômicas visíveis
- Comente sobre a qualidade da visualização
- Avalie a dissecção e exposição dos tecidos

## ⏱️ Linha do Tempo - Momentos Críticos
[Para cada momento crítico, forneça:
- Timestamp exato
- Descrição do evento
- Instrumentos envolvidos
- Recomendação específica]

## 💡 Recomendações Técnicas
1. [Recomendação baseada em instrumentação]
2. [Recomendação baseada em técnica cirúrgica]
3. [Recomendação baseada em segurança]
4. [Recomendação para follow-up ou revisão]

## ⚙️ Limitações da Análise Automatizada
[Parágrafo claro sobre:
- Limitações do sistema de visão computacional
- Necessidade de revisão por cirurgião especialista
- Contexto clínico não disponível para a IA]

## ⚖️ Disclaimer Médico-Legal
**IMPORTANTE:** Este relatório foi gerado pelo sistema **Gemini 2.5 Flash** e não substitui avaliação médica profissional. Todas as detecções devem ser validadas por especialista qualificado em cirurgia ginecológica. O uso deste relatório é de responsabilidade exclusiva do profissional solicitante.

---

**DIRETRIZES CRÍTICAS**
- Use terminologia médica apropriada e precisa
- Seja ESPECÍFICO ao mencionar instrumentos - evite termos genéricos
- Para cada anomalia, explique o que foi detectado e sua relevância clínica
- Inclua timestamps sempre que mencionar eventos
- Máximo 800 palavras para permitir análise detalhada
- Use emojis nos títulos para melhor organização visual
"""
        
        return prompt
    
    def _build_audio_prompt(self, analysis_result: AudioAnalysisResult) -> str:
        """
        Constrói o prompt estruturado para geração de relatório de áudio.
        
        Args:
            analysis_result: Dados da análise de áudio.
        
        Returns:
            Prompt formatado para o Gemini.
        """
        # Agrupa indicadores por tipo
        indicator_counts = {}
        for segment in analysis_result.segments:
            for indicator in segment.indicators:
                indicator_counts[indicator] = indicator_counts.get(indicator, 0) + 1
        
        # Identifica momentos de maior risco
        high_risk_segments = [
            s for s in analysis_result.segments 
            if s.confidence > 0.6 and len(s.indicators) > 0
        ][:5]
        
        # Contexto específico por tipo de consulta
        consultation_context = {
            "gynecological": "consulta ginecológica de rotina ou investigação de sintomas",
            "prenatal": "acompanhamento pré-natal e saúde gestacional",
            "postpartum": "consulta pós-parto e triagem de depressão puerperal",
            "general": "consulta médica geral em saúde da mulher"
        }
        
        context_desc = consultation_context.get(
            analysis_result.consultation_type.value if hasattr(analysis_result, 'consultation_type') else 'general',
            consultation_context["general"]
        )
        
        # Calcula timestamps críticos
        critical_timestamps = [
            f"{s.start_time:.1f}s-{s.end_time:.1f}s (confiança: {s.confidence:.0%})"
            for s in high_risk_segments
        ]
        
        # Informações da paciente para personalização
        patient_context = ""
        primeiro_nome = "paciente"  # Valor padrão
        if analysis_result.patient_data:
            pd = analysis_result.patient_data
            primeiro_nome = pd.nome.split()[0] if pd.nome else "paciente"
            
            patient_context = f"""
**INFORMAÇÕES DA PACIENTE**
- Nome: {primeiro_nome}
- Idade: {pd.idade} anos
- Histórico gestacional: {"Primeira gestação" if not pd.ja_foi_mae else f"{pd.numero_gestacoes}ª gestação"}
- Telefone: {pd.telefone}
"""
            if pd.endereco:
                patient_context += f"- Endereço: {pd.endereco}\n"
        
        # Formata data e hora da análise
        agora = datetime.now()
        data_analise = agora.strftime("%d/%m/%Y - %H:%M")
        
        # Tipo de consulta por extenso
        consultation_type_display = {
            "gynecological": "Ginecológica",
            "prenatal": "Pré-natal",
            "postpartum": "Pós-parto e Triagem de Depressão Puerperal",
            "general": "Geral em Saúde da Mulher"
        }[analysis_result.consultation_type.value if hasattr(analysis_result, 'consultation_type') else 'general']
        
        prompt = f"""
Você é um psicólogo especialista em **saúde mental da mulher** e análise de voz computacional aplicada à medicina.

**CONTEXTO CLÍNICO**
Tipo de consulta: {context_desc.upper()}
{patient_context}
**DADOS DA ANÁLISE ACÚSTICA**

- Arquivo: {analysis_result.filename}
- Duração total: {analysis_result.duration_seconds:.1f} segundos ({analysis_result.duration_seconds // 60:.0f}min {analysis_result.duration_seconds % 60:.0f}s)
- Segmentos analisados: {len(analysis_result.segments)}
- Nível de risco geral: **{analysis_result.overall_risk_level.upper()}**
- Data da análise: {data_analise}h

**INDICADORES PSICOLÓGICOS DETECTADOS**
{self._format_indicator_summary(indicator_counts)}

**SEGMENTOS DE ALTO RISCO**
{len(high_risk_segments)} segmentos com confiança > 60%
Timestamps críticos: {', '.join(critical_timestamps) if critical_timestamps else 'Nenhum'}

---

**TAREFA**

Gere um laudo psicológico DETALHADO em português (pt-BR) seguindo a estrutura:

**IMPORTANTE: O relatório DEVE começar com o seguinte cabeçalho EXATAMENTE formatado:**

Laudo Psicológico - Análise Vocal Computacional
Paciente: {primeiro_nome}
Idade: {analysis_result.patient_data.idade if analysis_result.patient_data else '[idade não informada]'} anos
Tipo de Consulta: {consultation_type_display}
Data da Análise: {data_analise}h
Nível de Risco Geral Detectado: {analysis_result.overall_risk_level.upper()}

---

## 🎤 Perfil Vocal e Características Acústicas
- Descreva tom médio (grave/agudo), variação de pitch
- Análise de energia vocal (fraca/forte, variação)
- Ritmo da fala (lenta/rápida, pausas frequentes)
- Qualidade vocal (tremor, quebras, estabilidade)

## 🧠 Indicadores Psicológicos Identificados

### 😔 Depressão / Depressão Pós-Parto
- **SE DETECTADO**: Descreva padrões específicos (tom baixo, monotonia, silêncios prolongados, falta de energia)
- **SE NÃO DETECTADO**: Mencione brevemente que não foram identificados padrões característicos
- Correlacione com o contexto da consulta

### 😰 Ansiedade / Ansiedade Gestacional
- **SE DETECTADO**: Descreva manifestações (variação rápida de pitch, fala acelerada, tremor vocal, alta energia)
- **SE NÃO DETECTADO**: Confirme ausência de padrões ansiosos
- Para consultas pré-natais, abordar ansiedade gestacional especificamente

### 🗣️ Hesitação e Distress Vocal
- Análise de pausas, hesitações ao relatar sintomas
- Tremor ou instabilidade vocal
- Possíveis dificuldades em expressar desconforto

### ⚠️ Sinais de Alerta (Trauma/Violência)
- **SE DETECTADO**: Abordar com MÁXIMA SENSIBILIDADE
- Padrões de hesitação extrema, quedas abruptas de energia
- Inconsistências emocionais
- **Sempre sugerir encaminhamento para serviço especializado**

## ⏱️ Linha do Tempo - Momentos Críticos
[Para cada segmento de alto risco, forneça:
- Timestamp exato (início-fim)
- Indicadores detectados
- Descrição do padrão vocal
- Possível significado clínico]

## 💡 Interpretação Clínica Integrada
[Parágrafo conectando os achados acústicos com:
- Contexto do tipo de consulta
- Possíveis condições subjacentes
- Necessidade de investigação adicional]

## 🩺 Recomendações para Acompanhamento
1. [Recomendação baseada em indicadores específicos detectados]
2. [Sugestão de avaliação complementar se necessário]
3. [Orientação sobre follow-up e periodicidade]
4. [Encaminhamentos para especialistas se indicado]
5. [Medidas de suporte imediato se risco identificado]

## ⚙️ Limitações da Análise Automatizada
[Parágrafo claro sobre:
- Limitações da análise acústica computacional
- Impossibilidade de captar contexto verbal completo
- Necessidade de avaliação presencial por profissional
- Fatores que podem influenciar padrões vocais (qualidade do áudio, ruído, etc.)]

## ⚖️ Disclaimer Médico-Legal
**IMPORTANTE:** Este relatório foi gerado pelo sistema **Gemini 2.5 Flash** baseado em análise acústica automatizada. **NÃO constitui diagnóstico clínico** e deve ser interpretado exclusivamente por profissional de saúde mental qualificado. Em caso de risco iminente identificado, contate imediatamente serviços de emergência (CVV 188, SAMU 192) ou Delegacia da Mulher.

---

**DIRETRIZES CRÍTICAS**
- **CABEÇALHO OBRIGATÓRIO**: O relatório DEVE começar EXATAMENTE com o cabeçalho formatado especificado acima, com cada campo em uma linha separada
- **PERSONALIZAÇÃO**: Se houver dados da paciente, use APENAS o primeiro nome dela conforme informado (ex: "A análise de {primeiro_nome} detectou...", "{primeiro_nome} apresenta padrões vocais...")
- **IMPORTANTE**: NÃO INVENTE NOMES. Se não houver nome da paciente nos dados acima, use apenas "a paciente" ou "paciente"
- **CONTEXTO GESTACIONAL**: Se for primeira gestação, mencione que pode ser um momento de maior ansiedade natural; se for mãe experiente, contextualize com base nisso
- Linguagem técnica mas compassiva e acolhedora
- Baseado EXCLUSIVAMENTE em padrões acústicos objetivos (não invente informações verbais)
- Máximo 700 palavras para análise completa e detalhada
- Enfatizar SEMPRE necessidade de avaliação presencial
- Se houver risco alto, destacar claramente necessidade de ação imediata
"""
        
        return prompt
    
    def _format_anomaly_summary(self, summary: dict[str, int]) -> str:
        """Formata o sumário de anomalias para o prompt."""
        if not summary:
            return "Nenhuma anomalia detectada"
        
        lines = []
        for anomaly_type, count in summary.items():
            anomaly_name = anomaly_type.replace("_", " ").title()
            lines.append(f"- {anomaly_name}: {count} ocorrência(s)")
        
        return "\n".join(lines)
    
    def _format_detailed_findings(self, analysis_result: VideoAnalysisResult) -> str:
        """Formata achados detalhados por categoria."""
        if not analysis_result.anomaly_summary:
            return "### ✅ Sem Anomalias\n\nNenhuma anomalia ou evento adverso foi detectado durante a análise do procedimento cirúrgico."
        
        findings = []
        
        # Mapeamento de tipos de anomalia para emoji e descrição
        anomaly_info = {
            "instrument_detected": ("🔧", "Instrumentos Cirúrgicos", "Instrumentos cirúrgicos foram detectados nas cenas analisadas."),
            "bleeding": ("🩸", "Sangramento", "Presença de sangramento identificada durante o procedimento."),
            "excessive_bleeding": ("🚨", "Sangramento Excessivo", "Sangramento de alta intensidade detectado - requer atenção imediata."),
            "abnormal_movement": ("⚠️", "Movimento Anormal", "Movimentos fora do padrão esperado foram identificados."),
            "instrument_misuse": ("❌", "Uso Inadequado de Instrumento", "Possível uso inadequado ou posicionamento incorreto de instrumento."),
            "poor_visibility": ("👁️", "Visibilidade Comprometida", "Campo cirúrgico com visibilidade reduzida (sangue, condensação, obstrução)."),
            "tissue_damage": ("🔴", "Lesão Tecidual", "Possível lesão ou trauma tecidual detectado."),
        }
        
        for anomaly_type, count in analysis_result.anomaly_summary.items():
            emoji, title, description = anomaly_info.get(
                anomaly_type.lower(),
                ("⚡", anomaly_type.replace("_", " ").title(), "Evento detectado pelo sistema de análise.")
            )
            
            findings.append(f"### {emoji} {title}")
            findings.append(f"**Ocorrências:** {count}")
            findings.append(f"**Descrição:** {description}")
            findings.append("")  # Linha em branco
        
        return "\n".join(findings)
    
    def _format_instruments_section(self, instruments: list[str], analysis_result: VideoAnalysisResult) -> str:
        """Formata a seção de instrumentos detectados."""
        if not instruments:
            return "Nenhum instrumento cirúrgico específico foi identificado nas detecções."
        
        # Contagem de aparições por instrumento
        instrument_counts = {}
        for frame in analysis_result.frames:
            for det in frame.detections:
                instrument_counts[det.class_name] = instrument_counts.get(det.class_name, 0) + 1
        
        lines = ["| Instrumento | Detecções | Frequência |"]
        lines.append("|------------|-----------|------------|")
        
        total_detections = sum(instrument_counts.values())
        for instrument, count in sorted(instrument_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_detections * 100) if total_detections > 0 else 0
            display_name = instrument.replace("_", " ").title()
            lines.append(f"| {display_name} | {count} | {percentage:.1f}% |")
        
        lines.append("")
        lines.append(f"**Total de detecções:** {total_detections}")
        
        return "\n".join(lines)
    
    def _format_temporal_distribution(self, analysis_result: VideoAnalysisResult) -> str:
        """Formata distribuição temporal das detecções."""
        if not analysis_result.frames:
            return "Sem dados de distribuição temporal disponíveis."
        
        # Divide o vídeo em quartis
        duration = analysis_result.duration_seconds
        quartiles = [(0, duration/4), (duration/4, duration/2), (duration/2, 3*duration/4), (3*duration/4, duration)]
        quartile_names = ["🕐 Primeiro Quarto", "🕑 Segundo Quarto", "🕒 Terceiro Quarto", "🕓 Quarto Final"]
        
        lines = []
        for (start, end), name in zip(quartiles, quartile_names):
            frames_in_quartile = [
                f for f in analysis_result.frames 
                if start <= f.timestamp_seconds < end
            ]
            detections_in_quartile = sum(len(f.detections) for f in frames_in_quartile)
            critical_in_quartile = len([f for f in frames_in_quartile if f.severity == "critical"])
            
            lines.append(f"**{name}** ({start:.1f}s - {end:.1f}s)")
            lines.append(f"  - Frames analisados: {len(frames_in_quartile)}")
            lines.append(f"  - Detecções: {detections_in_quartile}")
            lines.append(f"  - Frames críticos: {critical_in_quartile}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _extract_instruments_info(self, analysis_result: VideoAnalysisResult) -> str:
        """
        Extrai informações detalhadas dos instrumentos detectados com bounding boxes.
        
        Args:
            analysis_result: Resultado da análise de vídeo.
        
        Returns:
            String formatada com informações dos instrumentos.
        """
        # Coleta todas as detecções de instrumentos
        instrument_detections = []
        
        for frame in analysis_result.frames:
            for bbox in frame.bounding_boxes:
                # Formata o nome do instrumento corretamente
                instrument_name = bbox.label.replace("_", " ").title()
                
                instrument_detections.append({
                    'name': instrument_name,
                    'timestamp': frame.timestamp_seconds,
                    'confidence': bbox.confidence,
                    'frame_index': frame.frame_index,
                    'severity': frame.severity
                })
        
        if not instrument_detections:
            return "**INSTRUMENTOS DETECTADOS (BOUNDING BOXES DO YOLO)**\n\nNenhum instrumento foi detectado pelo sistema de visão computacional neste vídeo."
        
        # Agrupa por tipo de instrumento
        instruments_by_type = {}
        for det in instrument_detections:
            name = det['name']
            if name not in instruments_by_type:
                instruments_by_type[name] = {
                    'count': 0,
                    'avg_confidence': 0.0,
                    'timestamps': []
                }
            instruments_by_type[name]['count'] += 1
            instruments_by_type[name]['avg_confidence'] += det['confidence']
            # Adiciona apenas primeiras 10 ocorrências para não sobrecarregar
            if len(instruments_by_type[name]['timestamps']) < 10:
                instruments_by_type[name]['timestamps'].append({
                    'time': det['timestamp'],
                    'confidence': det['confidence'],
                    'severity': det['severity']
                })
        
        # Calcula média de confiança
        for name in instruments_by_type:
            count = instruments_by_type[name]['count']
            instruments_by_type[name]['avg_confidence'] /= count
        
        # Formata output
        lines = ["**INSTRUMENTOS DETECTADOS (BOUNDING BOXES DO YOLO)**"]
        lines.append("")
        lines.append("⚠️ **IMPORTANTE**: Estes instrumentos foram detectados automaticamente pelo sistema YOLOv8.")
        lines.append("Use estas informações para criar uma análise detalhada da instrumentação cirúrgica.")
        lines.append("")
        
        # Ordena por quantidade de detecções
        sorted_instruments = sorted(
            instruments_by_type.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        for instrument_name, info in sorted_instruments:
            lines.append(f"### 🔧 {instrument_name}")
            lines.append(f"- **Total de detecções**: {info['count']}")
            lines.append(f"- **Confiança média**: {info['avg_confidence']:.1%}")
            
            # Lista timestamps
            if info['timestamps']:
                timestamp_strs = []
                for ts_info in info['timestamps'][:5]:  # Primeiros 5
                    timestamp_strs.append(
                        f"{ts_info['time']:.1f}s (conf: {ts_info['confidence']:.1%}, sev: {ts_info['severity']})"
                    )
                
                if info['count'] > 5:
                    timestamp_strs.append(f"... e mais {info['count'] - 5} detecções")
                
                lines.append(f"- **Primeiras aparições**: {', '.join(timestamp_strs)}")
            
            lines.append("")
        
        lines.append(f"**TOTAL**: {len(instrument_detections)} detecções de instrumentos em {len(sorted_instruments)} tipos diferentes")
        lines.append("")
        
        return "\n".join(lines)
    
    def _format_indicator_summary(self, indicators: dict[str, int]) -> str:
        """Formata o sumário de indicadores psicológicos."""
        if not indicators:
            return "Nenhum indicador de risco detectado"
        
        lines = []
        for indicator, count in indicators.items():
            indicator_name = indicator.replace("_", " ").title()
            lines.append(f"- {indicator_name}: {count} segmento(s)")
        
        return "\n".join(lines)
    
    async def _generate_with_retry(
        self,
        prompt: str,
        max_retries: Optional[int] = None
    ) -> str:
        """
        Gera conteúdo com retry automático e backoff exponencial.
        
        Args:
            prompt: Prompt para o Gemini.
            max_retries: Número máximo de tentativas (usa config se None).
        
        Returns:
            Texto gerado pelo modelo.
        
        Raises:
            Exception: Se todas as tentativas falharem.
        """
        if max_retries is None:
            max_retries = settings.GEMINI_MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Tentativa {attempt + 1}/{max_retries} de chamada à API Gemini")
                # Chamada assíncrona ao Gemini
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt
                )
                logger.debug(f"Resposta recebida do Gemini com sucesso")
                return response.text
            
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Erro na tentativa {attempt + 1}/{max_retries}: {error_msg}")
                
                # Verifica se é rate limit (429) ou erro temporário
                if "429" in error_msg or "quota" in error_msg.lower():
                    if attempt < max_retries - 1:
                        # Backoff exponencial: 1s, 2s, 4s...
                        delay = settings.GEMINI_RETRY_DELAY * (2 ** attempt)
                        logger.warning(
                            f"Rate limit atingido. Tentativa {attempt + 1}/{max_retries}. "
                            f"Aguardando {delay}s..."
                        )
                        await asyncio.sleep(delay)
                        continue
                
                # Se não é rate limit ou esgotou tentativas, propaga erro
                logger.error(f"Erro ao chamar Gemini API (tentativa {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
    
    def _generate_fallback_video_report(self, analysis_result: VideoAnalysisResult) -> str:
        """
        Gera relatório de fallback quando a API Gemini falha.
        
        Args:
            analysis_result: Dados da análise.
        
        Returns:
            Relatório básico estruturado sem LLM.
        """
        total_anomalies = sum(analysis_result.anomaly_summary.values())
        
        # Calcula estatísticas detalhadas
        critical_frames = [f for f in analysis_result.frames if f.severity == "critical"]
        high_severity_frames = [f for f in analysis_result.frames if f.severity == "high"]
        medium_severity_frames = [f for f in analysis_result.frames if f.severity == "medium"]
        
        # Identifica instrumentos detectados
        instruments_detected = []
        for frame in analysis_result.frames:
            for det in frame.detections:
                if det.class_name not in instruments_detected:
                    instruments_detected.append(det.class_name)
        
        # Monta seção de achados detalhada
        detailed_findings = self._format_detailed_findings(analysis_result)
        
        return f"""# 🏥 Relatório de Análise de Vídeo Cirúrgico
**Gerado por: Gemini 2.5 Flash** | Data: {analysis_result.created_at.strftime('%d/%m/%Y %H:%M:%S') if hasattr(analysis_result, 'created_at') else 'N/A'}

---

## 📋 Sumário Executivo

**Arquivo analisado:** `{analysis_result.filename}`  
**Duração do vídeo:** {analysis_result.duration_seconds:.1f} segundos ({analysis_result.duration_seconds // 60:.0f}min {analysis_result.duration_seconds % 60:.0f}s)  
**Frames processados:** {analysis_result.total_frames_analyzed}  
**Taxa de amostragem:** ~{analysis_result.total_frames_analyzed / analysis_result.duration_seconds:.1f} frames/segundo

### 🎯 Resultados da Análise
- **Total de detecções:** {total_anomalies}
- **Frames críticos:** {len(critical_frames)}
- **Frames alta severidade:** {len(high_severity_frames)}
- **Frames média severidade:** {len(medium_severity_frames)}

---

## 🔍 Achados Detalhados

{detailed_findings}

---

## 🔧 Instrumentos Identificados

{self._format_instruments_section(instruments_detected, analysis_result)}

---

## ⏱️ Distribuição Temporal

{self._format_temporal_distribution(analysis_result)}

---

## ⚠️ Observações Importantes

> **ℹ️ Modo de Geração:** Este relatório foi gerado automaticamente em **modo simplificado** devido à indisponibilidade temporária do serviço de análise avançada com IA generativa.

**Recomendações:**
1. ✅ Revisar manualmente todos os frames com severidade crítica
2. ✅ Validar as detecções de instrumentos em contexto clínico
3. ✅ Correlacionar achados com prontuário e histórico do paciente
4. ✅ Solicitar nova análise com IA generativa quando disponível para insights adicionais

---

## ⚖️ Disclaimer Médico-Legal

**⚠️ IMPORTANTE:** Este relatório foi gerado por sistema de visão computacional baseado em **YOLOv8** e **Gemini 2.5 Flash**. As detecções são probabilísticas e **NÃO substituem avaliação médica profissional**.

**Responsabilidades:**
- ✓ Todas as detecções devem ser **validadas por especialista qualificado**
- ✓ O sistema pode gerar **falsos positivos e falsos negativos**
- ✓ A decisão clínica final é **exclusivamente do profissional médico**
- ✓ Use este relatório como **ferramenta auxiliar**, não como diagnóstico definitivo

**Em caso de dúvidas ou achados críticos, consulte imediatamente um cirurgião ginecológico.**
"""
    
    def _generate_fallback_audio_report(self, analysis_result: AudioAnalysisResult) -> str:
        """Gera relatório de fallback para áudio com formatação enriquecida."""
        
        # Contexto da consulta
        consultation_names = {
            "gynecological": "Consulta Ginecológica",
            "prenatal": "Acompanhamento Pré-Natal",
            "postpartum": "Consulta Pós-Parto",
            "general": "Consulta Geral"
        }
        
        consultation_name = consultation_names.get(
            analysis_result.consultation_type.value if hasattr(analysis_result, 'consultation_type') else 'general',
            "Consulta Médica"
        )
        
        # Agrupa indicadores
        indicator_counts = {}
        for segment in analysis_result.segments:
            for indicator in segment.indicators:
                indicator_counts[indicator] = indicator_counts.get(indicator, 0) + 1
        
        # Segmentos por nível de risco
        high_confidence_segments = [s for s in analysis_result.segments if s.confidence > 0.7]
        medium_confidence_segments = [s for s in analysis_result.segments if 0.5 < s.confidence <= 0.7]
        
        # Monta descrição dos indicadores
        indicator_descriptions = self._format_audio_indicators_detailed(indicator_counts)
        
        # Nível de risco com emoji
        risk_emoji = {
            "none": "✅",
            "low": "🟡",
            "medium": "🟠",
            "high": "🔴"
        }
        
        risk_icon = risk_emoji.get(analysis_result.overall_risk_level.value, "⚪")
        
        return f"""# 🎤 Relatório de Análise de Áudio - {consultation_name}
**Gerado por: Gemini 2.5 Flash** | Data: {analysis_result.created_at.strftime('%d/%m/%Y %H:%M:%S') if hasattr(analysis_result, 'created_at') else 'N/A'}

---

## 📋 Sumário Executivo

**Arquivo analisado:** `{analysis_result.filename}`  
**Tipo de consulta:** {consultation_name}  
**Duração do áudio:** {analysis_result.duration_seconds:.1f} segundos ({analysis_result.duration_seconds // 60:.0f}min {analysis_result.duration_seconds % 60:.0f}s)  
**Segmentos processados:** {len(analysis_result.segments)}  
**Nível de risco identificado:** {risk_icon} **{analysis_result.overall_risk_level.upper()}**

---

## 🧠 Indicadores Psicológicos Detectados

{indicator_descriptions}

---

## 📊 Análise de Segmentos

**Distribuição por confiança:**
- 🔴 Alta confiança (>70%): {len(high_confidence_segments)} segmentos
- 🟠 Média confiança (50-70%): {len(medium_confidence_segments)} segmentos
- 🟢 Baixa confiança (<50%): {len(analysis_result.segments) - len(high_confidence_segments) - len(medium_confidence_segments)} segmentos

{self._format_audio_timeline(analysis_result.segments[:5])}

---

## 💡 Interpretação Preliminar

{self._generate_audio_interpretation(analysis_result.overall_risk_level.value, consultation_name, indicator_counts)}

---

## 🩺 Recomendações de Acompanhamento

{self._generate_audio_recommendations(analysis_result.overall_risk_level.value, indicator_counts)}

---

## ⚠️ Observações Importantes

> **ℹ️ Modo de Geração:** Este relatório foi gerado automaticamente em **modo simplificado** devido à indisponibilidade temporária do serviço de análise avançada com IA generativa.

**Checklist para o profissional:**
1. ✅ Revisar contexto clínico completo da paciente
2. ✅ Considerar fatores situacionais que podem afetar padrões vocais
3. ✅ Avaliar histórico psicológico e psiquiátrico prévio
4. ✅ Realizar avaliação presencial detalhada
5. ✅ Solicitar nova análise com IA generativa quando disponível

---

## ⚖️ Disclaimer Médico-Legal

**⚠️ IMPORTANTE:** Este relatório foi gerado por sistema de análise acústica baseado em **Gemini 2.5 Flash** e **NÃO constitui diagnóstico clínico**. Todos os indicadores detectados são probabilísticos e devem ser interpretados exclusivamente por profissional de saúde mental qualificado.

**Em caso de crise ou risco iminente:**
- 📞 CVV (Centro de Valorização da Vida): **188**
- 🚑 SAMU: **192**
- 👮 Delegacia da Mulher ou Polícia Militar: **190**
- 💬 Disque 180: Atendimento à mulher em situação de violência

**O uso deste relatório é de responsabilidade exclusiva do profissional solicitante.**
"""
    
    def _format_audio_indicators_detailed(self, indicator_counts: dict) -> str:
        """Formata indicadores de áudio com descrições detalhadas."""
        if not indicator_counts:
            return "### ✅ Nenhum Indicador de Risco Detectado\\n\\nA análise acústica não identificou padrões vocais associados a indicadores psicológicos de risco."
        
        indicator_info = {
            "depression_indicator": ("😔", "Depressão / Depressão Pós-Parto", "Tom vocal baixo, monotonia, baixa energia, silêncios prolongados"),
            "anxiety_indicator": ("😰", "Ansiedade / Ansiedade Gestacional", "Variação rápida de pitch, fala acelerada, tremor vocal, alta energia"),
            "vocal_distress": ("🗣️", "Distress Vocal / Hesitação", "Pausas frequentes, hesitações, instabilidade vocal, dificuldade em expressar-se"),
            "domestic_violence_indicator": ("🚨", "Sinais de Alerta (Trauma)", "Hesitação extrema, quedas abruptas de energia, inconsistências emocionais")
        }
        
        lines = []
        for indicator, count in indicator_counts.items():
            emoji, title, description = indicator_info.get(
                indicator.value if hasattr(indicator, 'value') else str(indicator),
                ("⚡", indicator.replace("_", " ").title(), "Indicador detectado")
            )
            
            lines.append(f"### {emoji} {title}")
            lines.append(f"**Ocorrências:** {count} segmentos")
            lines.append(f"**Características:** {description}")
            lines.append("")
        
        return "\\n".join(lines)
    
    def _format_audio_timeline(self, segments: list) -> str:
        """Formata linha do tempo dos principais segmentos."""
        if not segments:
            return ""
        
        lines = ["\\n## ⏱️ Linha do Tempo - Principais Segmentos\\n"]
        
        for i, seg in enumerate(segments, 1):
            if seg.indicators:
                indicators_str = ", ".join([ind.value.replace("_", " ").title() for ind in seg.indicators])
                lines.append(f"**Segmento {i}:** {seg.start_time:.1f}s - {seg.end_time:.1f}s")
                lines.append(f"  - Indicadores: {indicators_str}")
                lines.append(f"  - Confiança: {seg.confidence:.0%}")
                lines.append("")
        
        return "\\n".join(lines) if len(lines) > 1 else ""
    
    def _generate_audio_interpretation(self, risk_level: str, consultation_type: str, indicators: dict) -> str:
        """Gera interpretação textual baseada no risco."""
        if risk_level == "none":
            return f"A análise acústica da {consultation_type.lower()} não identificou padrões vocais significativos associados a indicadores de risco psicológico. Os parâmetros de pitch, energia e ritmo de fala encontram-se dentro de faixas esperadas."
        
        if risk_level == "low":
            return f"A análise identificou indicadores leves que sugerem monitoramento de rotina. Durante a {consultation_type.lower()}, foram detectados padrões vocais sutis que podem estar relacionados a variações emocionais normais ou situacionais."
        
        if risk_level == "medium":
            return f"A análise detectou padrões vocais moderados que recomendam avaliação clínica mais detalhada. Os indicadores identificados durante a {consultation_type.lower()} sugerem possível sofrimento psicológico que merece atenção profissional."
        
        if risk_level == "high":
            return f"⚠️ **ATENÇÃO:** A análise identificou padrões vocais significativos que indicam necessidade de avaliação urgente. Os indicadores detectados durante a {consultation_type.lower()} sugerem sofrimento psicológico importante. **Recomenda-se encaminhamento imediato para profissional de saúde mental.**"
        
        return "Análise inconclusiva."
    
    def _generate_audio_recommendations(self, risk_level: str, indicators: dict) -> str:
        """Gera recomendações baseadas no risco."""
        recommendations = []
        
        if risk_level == "none" or risk_level == "low":
            recommendations.append("1. ✅ Manter acompanhamento de rotina conforme protocolo")
            recommendations.append("2. ✅ Estar atento a mudanças no padrão emocional em consultas futuras")
            recommendations.append("3. ✅ Oferecer espaço seguro para expressão de preocupações")
        else:
            recommendations.append("1. 🩺 **Avaliação presencial detalhada por psicólogo/psiquiatra**")
            recommendations.append("2. 📋 Aplicar escalas validadas (Edinburgh, GAD-7, PHQ-9 conforme indicação)")
            
            if any("depression" in str(ind).lower() for ind in indicators):
                recommendations.append("3. 💊 Considerar avaliação para depressão pós-parto (se aplicável)")
            
            if any("anxiety" in str(ind).lower() for ind in indicators):
                recommendations.append("3. 😰 Investigar transtornos de ansiedade e ansiedade gestacional")
            
            if any("violence" in str(ind).lower() or "trauma" in str(ind).lower() for ind in indicators):
                recommendations.append("4. 🚨 **PRIORIDADE:** Avaliar contexto de violência doméstica em ambiente seguro")
                recommendations.append("5. 🏥 Acionar rede de proteção e encaminhar para serviços especializados")
            
            if risk_level == "high":
                recommendations.append(f"{len(recommendations) + 1}. ⏰ **Acompanhamento urgente: agendar retorno em até 48-72h**")
        
        return "\\n".join(recommendations)


# Singleton global
_gemini_service_instance: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
    """
    Obtém a instância singleton do GeminiService.
    
    Returns:
        Instância inicializada do GeminiService.
    """
    global _gemini_service_instance
    if _gemini_service_instance is None:
        _gemini_service_instance = GeminiService()
    return _gemini_service_instance
