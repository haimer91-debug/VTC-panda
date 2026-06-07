import { useState, useEffect, useCallback } from 'react';
import {
  StyleSheet, Text, View, TextInput, TouchableOpacity,
  FlatList, ActivityIndicator, I18nManager, SafeAreaView,
  ScrollView, KeyboardAvoidingView, Platform, Modal,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as DocumentPicker from 'expo-document-picker';
import { API_URL } from './config';
import { t, LANGS } from './i18n';

I18nManager.allowRTL(true);

// ── Tiny API helper ───────────────────────────────────────────────────────────
async function api(path, opts = {}) {
  const r = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function uploadFile(userId, file) {
  const form = new FormData();
  form.append('file', { uri: file.uri, name: file.name, type: file.mimeType || 'application/octet-stream' });
  const r = await fetch(`${API_URL}/users/${userId}/import`, { method: 'POST', body: form });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

export default function App() {
  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState('');
  const [tab, setTab] = useState('sessions');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [lang, setLang] = useState('he');
  const cycleLang = () => setLang((l) => LANGS[(LANGS.indexOf(l) + 1) % LANGS.length]);

  const login = async () => {
    if (!username.trim()) return;
    setLoading(true); setError('');
    try {
      const data = await api('/auth/login', {
        method: 'POST', body: JSON.stringify({ username: username.trim() }),
      });
      setUserId(data.user_id);
    } catch {
      setError(t(lang, 'loginError'));
    } finally { setLoading(false); }
  };

  const logout = () => { setUserId(null); setUsername(''); setTab('sessions'); };

  if (!userId) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" />
        <TouchableOpacity onPress={cycleLang} style={styles.langBtn}>
          <Text style={styles.langBtnText}>{lang.toUpperCase()}</Text>
        </TouchableOpacity>
        <Text style={styles.logo}>🎾</Text>
        <Text style={styles.title}>{t(lang, 'appName')}</Text>
        <Text style={styles.subtitle}>{t(lang, 'loginPrompt')}</Text>
        <TextInput
          style={styles.input} placeholder={t(lang, 'username')} placeholderTextColor="#888"
          value={username} onChangeText={setUsername} autoCapitalize="none"
        />
        <TouchableOpacity style={styles.button} onPress={login} disabled={loading}>
          {loading ? <ActivityIndicator color="#111" /> : <Text style={styles.buttonText}>{t(lang, 'login')}</Text>}
        </TouchableOpacity>
        {!!error && <Text style={styles.error}>{error}</Text>}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      <View style={styles.topBar}>
        <TouchableOpacity onPress={logout}><Text style={styles.logout}>{t(lang, 'logout')}</Text></TouchableOpacity>
        <Text style={styles.topTitle}>🎾 {userId}</Text>
        <TouchableOpacity onPress={cycleLang} style={styles.langBtnSmall}>
          <Text style={styles.langBtnText}>{lang.toUpperCase()}</Text>
        </TouchableOpacity>
      </View>

      <View style={{ flex: 1 }}>
        {tab === 'sessions' && <SessionsScreen userId={userId} lang={lang} />}
        {tab === 'chat'     && <ChatScreen userId={userId} lang={lang} />}
        {tab === 'profile'  && <ProfileScreen userId={userId} lang={lang} />}
      </View>

      <View style={styles.tabBar}>
        <TabBtn active={tab === 'profile'}  label={t(lang, 'tabProfile')}  icon="⚙️" onPress={() => setTab('profile')} />
        <TabBtn active={tab === 'chat'}     label={t(lang, 'tabChat')}     icon="💬" onPress={() => setTab('chat')} />
        <TabBtn active={tab === 'sessions'} label={t(lang, 'tabSessions')} icon="🎬" onPress={() => setTab('sessions')} />
      </View>
    </SafeAreaView>
  );
}

function TabBtn({ active, label, icon, onPress }) {
  return (
    <TouchableOpacity style={styles.tabBtn} onPress={onPress}>
      <Text style={{ fontSize: 22 }}>{icon}</Text>
      <Text style={[styles.tabLabel, active && styles.tabLabelActive]}>{label}</Text>
    </TouchableOpacity>
  );
}

// ── Sessions ──────────────────────────────────────────────────────────────────
function SessionsScreen({ userId, lang }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try { setSessions(await api(`/users/${userId}/sessions?limit=30`)); }
    catch { setError(t(lang, 'sessionsError')); }
    finally { setLoading(false); }
  }, [userId, lang]);

  useEffect(() => { load(); }, [load]);

  return (
    <View style={{ flex: 1 }}>
      <Text style={styles.screenTitle}>{t(lang, 'sessionsTitle')}</Text>
      {!!error && <Text style={styles.error}>{error}</Text>}
      <FlatList
        data={sessions}
        keyExtractor={(it) => it.match_id}
        contentContainerStyle={{ paddingBottom: 16 }}
        onRefresh={load}
        refreshing={loading}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.card} onPress={() => setSelected(item)}>
            <Text style={styles.cardDate}>{item.date}</Text>
            <Text style={styles.cardStats}>{item.shots} {t(lang, 'shots')} · {item.stats?.in_pct ?? '—'}% IN</Text>
            {!!item.note?.opponent && <Text style={styles.cardOpp}>{t(lang, 'opponent')}: {item.note.opponent}</Text>}
          </TouchableOpacity>
        )}
        ListEmptyComponent={!loading && <Text style={styles.empty}>{t(lang, 'sessionsEmpty')}</Text>}
      />
      <Modal visible={!!selected} animationType="slide" transparent onRequestClose={() => setSelected(null)}>
        <View style={styles.modalBackdrop}>
          <View style={styles.modalSheet}>
            <Text style={styles.screenTitle}>{selected?.date}</Text>
            <ScrollView style={{ maxHeight: 360 }}>
              <Text style={styles.cardStats}>{t(lang, 'shots')}: {selected?.shots ?? '—'}</Text>
              <Text style={styles.cardStats}>{t(lang, 'rallies')}: {selected?.rallies ?? '—'}</Text>
              {selected?.stats && Object.entries(selected.stats).map(([k, v]) => (
                <Text key={k} style={styles.cardOpp}>{k}: {String(v)}</Text>
              ))}
              {!!selected?.note?.opponent && <Text style={styles.cardOpp}>{t(lang, 'opponent')}: {selected.note.opponent}</Text>}
              {!!selected?.note?.score && <Text style={styles.cardOpp}>{t(lang, 'score')}: {selected.note.score}</Text>}
            </ScrollView>
            <TouchableOpacity style={styles.button} onPress={() => setSelected(null)}>
              <Text style={styles.buttonText}>{t(lang, 'close')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ── Chat ──────────────────────────────────────────────────────────────────────
function ChatScreen({ userId, lang }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  const send = async () => {
    const text = input.trim();
    if (!text || sending) return;
    const next = [...messages, { role: 'user', content: text }];
    setMessages(next);
    setInput('');
    setSending(true);
    try {
      const r = await api(`/users/${userId}/chat`, {
        method: 'POST', body: JSON.stringify({ messages: next }),
      });
      setMessages([...next, { role: 'assistant', content: r.reply }]);
    } catch {
      setMessages([...next, { role: 'assistant', content: t(lang, 'chatError') }]);
    } finally { setSending(false); }
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <Text style={styles.screenTitle}>{t(lang, 'chatTitle')}</Text>
      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 12 }}>
        {messages.length === 0 && <Text style={styles.empty}>{t(lang, 'chatEmpty')}</Text>}
        {messages.map((m, i) => (
          <View key={i} style={[styles.bubble, m.role === 'user' ? styles.bubbleUser : styles.bubbleBot]}>
            <Text style={styles.bubbleText}>{m.content}</Text>
          </View>
        ))}
        {sending && <ActivityIndicator color="#BBFD00" style={{ marginTop: 8 }} />}
      </ScrollView>
      <View style={styles.chatInputRow}>
        <TouchableOpacity style={styles.sendBtn} onPress={send} disabled={sending}>
          <Text style={styles.sendBtnText}>{t(lang, 'send')}</Text>
        </TouchableOpacity>
        <TextInput
          style={styles.chatInput} placeholder={t(lang, 'chatPlaceholder')} placeholderTextColor="#888"
          value={input} onChangeText={setInput} multiline
        />
      </View>
    </KeyboardAvoidingView>
  );
}

// ── Profile ───────────────────────────────────────────────────────────────────
function ProfileScreen({ userId, lang }) {
  const [profile, setProfile] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    api(`/users/${userId}/profile`).then(setProfile).catch(() => {});
  }, [userId]);
  useEffect(() => { load(); }, [load]);

  const setSport = async (sport) => {
    if (saving || profile?.sport === sport) return;
    setSaving(true);
    setProfile((p) => ({ ...p, sport }));
    try {
      await api(`/users/${userId}/profile`, { method: 'PATCH', body: JSON.stringify({ sport }) });
    } catch {} finally { setSaving(false); }
  };

  return (
    <View style={{ flex: 1 }}>
      <Text style={styles.screenTitle}>{t(lang, 'profileTitle')}</Text>
      <View style={styles.card}>
        <Text style={styles.cardDate}>{t(lang, 'name')}: {profile?.username || userId}</Text>
        <Text style={styles.cardStats}>{t(lang, 'ntrpCurrent')}: {profile?.ntrp || '—'}</Text>
        <Text style={styles.cardStats}>{t(lang, 'ntrpNext')}: {profile?.ntrp_next || '—'}</Text>
      </View>

      <Text style={[styles.cardOpp, { marginTop: 18, textAlign: 'right' }]}>{t(lang, 'sport')}</Text>
      <View style={styles.sportRow}>
        <TouchableOpacity
          style={[styles.sportBtn, profile?.sport === 'padel' && styles.sportBtnActive]}
          onPress={() => setSport('padel')}>
          <Text style={[styles.sportBtnText, profile?.sport === 'padel' && styles.sportBtnTextActive]}>{t(lang, 'padel')} 🎾</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.sportBtn, profile?.sport === 'tennis' && styles.sportBtnActive]}
          onPress={() => setSport('tennis')}>
          <Text style={[styles.sportBtnText, profile?.sport === 'tennis' && styles.sportBtnTextActive]}>{t(lang, 'tennis')} 🎾</Text>
        </TouchableOpacity>
      </View>

      <ImportBox userId={userId} lang={lang} onImported={load} />
    </View>
  );
}

function ImportBox({ userId, lang, onImported }) {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState('');

  const pick = async () => {
    if (busy) return;
    setMsg('');
    const res = await DocumentPicker.getDocumentAsync({ multiple: false, copyToCacheDirectory: true });
    if (res.canceled || !res.assets?.length) return;
    const file = res.assets[0];
    setBusy(true);
    setMsg(t(lang, 'importing'));
    try {
      const r = await uploadFile(userId, file);
      const imported = r.imported ?? 0;
      const dup = r.skipped ?? r.duplicates ?? 0;
      setMsg(`${t(lang, 'importOk')}: ${imported}${dup ? ` (${dup} ${t(lang, 'importDup')})` : ''}`);
      onImported && onImported();
    } catch {
      setMsg(t(lang, 'importErr'));
    } finally { setBusy(false); }
  };

  return (
    <View style={{ marginTop: 18 }}>
      <Text style={[styles.cardOpp, { textAlign: 'right' }]}>{t(lang, 'importTitle')}</Text>
      <TouchableOpacity style={[styles.button, { marginTop: 8 }]} onPress={pick} disabled={busy}>
        {busy ? <ActivityIndicator color="#111" /> : <Text style={styles.buttonText}>{t(lang, 'importPick')}</Text>}
      </TouchableOpacity>
      {!!msg && <Text style={styles.cardOpp}>{msg}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#111', paddingHorizontal: 16, paddingTop: 50 },
  logo: { fontSize: 56, textAlign: 'center', marginBottom: 8 },
  title: { fontSize: 22, fontWeight: '900', color: '#fff', textAlign: 'center', marginBottom: 4 },
  subtitle: { fontSize: 14, color: '#aaa', textAlign: 'center', marginBottom: 24 },
  screenTitle: { fontSize: 18, fontWeight: '900', color: '#fff', textAlign: 'right', marginBottom: 10 },
  input: { backgroundColor: '#1e1e1e', color: '#fff', borderRadius: 10, padding: 14, marginBottom: 14, textAlign: 'right', fontSize: 16 },
  button: { backgroundColor: '#BBFD00', borderRadius: 10, padding: 14, alignItems: 'center' },
  buttonText: { color: '#111', fontWeight: '900', fontSize: 16 },
  error: { color: '#ff6b6b', textAlign: 'center', marginTop: 12 },
  card: { backgroundColor: '#1e1e1e', borderRadius: 12, padding: 16, marginTop: 10 },
  cardDate: { color: '#BBFD00', fontWeight: '700', fontSize: 15, textAlign: 'right' },
  cardStats: { color: '#fff', marginTop: 6, textAlign: 'right' },
  cardOpp: { color: '#aaa', marginTop: 4, textAlign: 'right' },
  empty: { color: '#888', textAlign: 'center', marginTop: 30 },
  topBar: { flexDirection: 'row-reverse', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 10 },
  topTitle: { color: '#fff', fontWeight: '900', fontSize: 17 },
  logout: { color: '#ff6b6b', fontSize: 14 },
  tabBar: { flexDirection: 'row-reverse', borderTopWidth: 1, borderTopColor: '#222', paddingTop: 8, paddingBottom: 6 },
  tabBtn: { flex: 1, alignItems: 'center' },
  tabLabel: { color: '#888', fontSize: 12, marginTop: 2 },
  tabLabelActive: { color: '#BBFD00', fontWeight: '700' },
  bubble: { borderRadius: 12, padding: 12, marginTop: 8, maxWidth: '85%' },
  bubbleUser: { backgroundColor: '#BBFD00', alignSelf: 'flex-end' },
  bubbleBot: { backgroundColor: '#1e1e1e', alignSelf: 'flex-start' },
  bubbleText: { color: '#111', textAlign: 'right' },
  chatInputRow: { flexDirection: 'row-reverse', alignItems: 'flex-end', paddingTop: 8, gap: 8 },
  chatInput: { flex: 1, backgroundColor: '#1e1e1e', color: '#fff', borderRadius: 10, padding: 12, textAlign: 'right', maxHeight: 100 },
  sendBtn: { backgroundColor: '#BBFD00', borderRadius: 10, paddingVertical: 12, paddingHorizontal: 18 },
  sendBtnText: { color: '#111', fontWeight: '900' },
  sportRow: { flexDirection: 'row-reverse', gap: 10, marginTop: 8 },
  sportBtn: { flex: 1, backgroundColor: '#1e1e1e', borderRadius: 10, paddingVertical: 14, alignItems: 'center', borderWidth: 1, borderColor: '#222' },
  sportBtnActive: { backgroundColor: '#BBFD00', borderColor: '#BBFD00' },
  sportBtnText: { color: '#888', fontWeight: '700' },
  sportBtnTextActive: { color: '#111' },
  modalBackdrop: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modalSheet: { backgroundColor: '#1e1e1e', borderTopLeftRadius: 18, borderTopRightRadius: 18, padding: 18, paddingBottom: 30 },
  langBtn: { position: 'absolute', top: 50, left: 16, backgroundColor: '#1e1e1e', borderRadius: 8, paddingVertical: 6, paddingHorizontal: 12 },
  langBtnSmall: { backgroundColor: '#1e1e1e', borderRadius: 8, paddingVertical: 4, paddingHorizontal: 10 },
  langBtnText: { color: '#BBFD00', fontWeight: '700', fontSize: 12 },
});
