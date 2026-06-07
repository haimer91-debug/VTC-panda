import { useState, useEffect, useCallback } from 'react';
import {
  StyleSheet, Text, View, TextInput, TouchableOpacity,
  FlatList, ActivityIndicator, I18nManager, SafeAreaView,
  ScrollView, KeyboardAvoidingView, Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { API_URL } from './config';

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

export default function App() {
  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState('');
  const [tab, setTab] = useState('sessions');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const login = async () => {
    if (!username.trim()) return;
    setLoading(true); setError('');
    try {
      const data = await api('/auth/login', {
        method: 'POST', body: JSON.stringify({ username: username.trim() }),
      });
      setUserId(data.user_id);
    } catch {
      setError('שגיאת התחברות, בדוק חיבור לאינטרנט');
    } finally { setLoading(false); }
  };

  const logout = () => { setUserId(null); setUsername(''); setTab('sessions'); };

  if (!userId) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" />
        <Text style={styles.logo}>🎾</Text>
        <Text style={styles.title}>Virtual Tennis Coach</Text>
        <Text style={styles.subtitle}>הזן שם משתמש כדי להמשיך</Text>
        <TextInput
          style={styles.input} placeholder="שם משתמש" placeholderTextColor="#888"
          value={username} onChangeText={setUsername} autoCapitalize="none"
        />
        <TouchableOpacity style={styles.button} onPress={login} disabled={loading}>
          {loading ? <ActivityIndicator color="#111" /> : <Text style={styles.buttonText}>כניסה</Text>}
        </TouchableOpacity>
        {!!error && <Text style={styles.error}>{error}</Text>}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      <View style={styles.topBar}>
        <TouchableOpacity onPress={logout}><Text style={styles.logout}>יציאה</Text></TouchableOpacity>
        <Text style={styles.topTitle}>🎾 {userId}</Text>
      </View>

      <View style={{ flex: 1 }}>
        {tab === 'sessions' && <SessionsScreen userId={userId} />}
        {tab === 'chat'     && <ChatScreen userId={userId} />}
        {tab === 'profile'  && <ProfileScreen userId={userId} />}
      </View>

      <View style={styles.tabBar}>
        <TabBtn active={tab === 'profile'}  label="פרופיל" icon="⚙️" onPress={() => setTab('profile')} />
        <TabBtn active={tab === 'chat'}     label="מאמן"   icon="💬" onPress={() => setTab('chat')} />
        <TabBtn active={tab === 'sessions'} label="אימונים" icon="🎬" onPress={() => setTab('sessions')} />
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
function SessionsScreen({ userId }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try { setSessions(await api(`/users/${userId}/sessions?limit=30`)); }
    catch { setError('שגיאה בטעינת אימונים'); }
    finally { setLoading(false); }
  }, [userId]);

  useEffect(() => { load(); }, [load]);

  return (
    <View style={{ flex: 1 }}>
      <Text style={styles.screenTitle}>האימונים שלי</Text>
      {!!error && <Text style={styles.error}>{error}</Text>}
      <FlatList
        data={sessions}
        keyExtractor={(it) => it.match_id}
        contentContainerStyle={{ paddingBottom: 16 }}
        onRefresh={load}
        refreshing={loading}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.cardDate}>{item.date}</Text>
            <Text style={styles.cardStats}>{item.shots} מכות · {item.stats?.in_pct ?? '—'}% IN</Text>
            {!!item.note?.opponent && <Text style={styles.cardOpp}>נגד: {item.note.opponent}</Text>}
          </View>
        )}
        ListEmptyComponent={!loading && <Text style={styles.empty}>אין עדיין אימונים, ייבא קובץ מהאתר</Text>}
      />
    </View>
  );
}

// ── Chat ──────────────────────────────────────────────────────────────────────
function ChatScreen({ userId }) {
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
      setMessages([...next, { role: 'assistant', content: 'שגיאה בקבלת תשובה, נסה שוב' }]);
    } finally { setSending(false); }
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <Text style={styles.screenTitle}>המאמן הוירטואלי</Text>
      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 12 }}>
        {messages.length === 0 && <Text style={styles.empty}>שאל אותי כל דבר על האימונים שלך</Text>}
        {messages.map((m, i) => (
          <View key={i} style={[styles.bubble, m.role === 'user' ? styles.bubbleUser : styles.bubbleBot]}>
            <Text style={styles.bubbleText}>{m.content}</Text>
          </View>
        ))}
        {sending && <ActivityIndicator color="#BBFD00" style={{ marginTop: 8 }} />}
      </ScrollView>
      <View style={styles.chatInputRow}>
        <TouchableOpacity style={styles.sendBtn} onPress={send} disabled={sending}>
          <Text style={styles.sendBtnText}>שלח</Text>
        </TouchableOpacity>
        <TextInput
          style={styles.chatInput} placeholder="כתוב הודעה" placeholderTextColor="#888"
          value={input} onChangeText={setInput} multiline
        />
      </View>
    </KeyboardAvoidingView>
  );
}

// ── Profile ───────────────────────────────────────────────────────────────────
function ProfileScreen({ userId }) {
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
      <Text style={styles.screenTitle}>הפרופיל שלי</Text>
      <View style={styles.card}>
        <Text style={styles.cardDate}>שם: {profile?.username || userId}</Text>
        <Text style={styles.cardStats}>NTRP נוכחי: {profile?.ntrp || '—'}</Text>
        <Text style={styles.cardStats}>NTRP יעד: {profile?.ntrp_next || '—'}</Text>
      </View>

      <Text style={[styles.cardOpp, { marginTop: 18, textAlign: 'right' }]}>ענף ספורט</Text>
      <View style={styles.sportRow}>
        <TouchableOpacity
          style={[styles.sportBtn, profile?.sport === 'padel' && styles.sportBtnActive]}
          onPress={() => setSport('padel')}>
          <Text style={[styles.sportBtnText, profile?.sport === 'padel' && styles.sportBtnTextActive]}>פאדל 🎾</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.sportBtn, profile?.sport === 'tennis' && styles.sportBtnActive]}
          onPress={() => setSport('tennis')}>
          <Text style={[styles.sportBtnText, profile?.sport === 'tennis' && styles.sportBtnTextActive]}>טניס 🎾</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.empty}>ייבוא קבצים יתווסף בקרוב</Text>
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
});
